#!/usr/bin/env python3
"""
道层教练干预手册验证脚本 v1.0
验证 pipeline-data/coaching-intervention-library.json 的合规性。

验证项:
  1. JSON 文件加载
  2. 四维度(C/M/E_exec/E_env)干预条目全覆盖
  3. 每条干预 intervention_id 格式合规
  4. applicable_stages ∈ [1,7]
  5. flywheel_support 值在六飞轮枚举内
  6. eight_step_ref ∈ [1,8] (若存在)
  7. flywheel_ref ∈ [1,6] (若存在)
  8. ⑤守护: iv-C-05 primary_sop='sop-05' + _dao_guard 存在
  9. intervention_selection_guide 存在
  10. validation_rules step_id_5_name='流程' + six_flywheel_valid_names 6个
"""

import json
import sys
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
LIB_PATH = REPO_ROOT / "pipeline-data" / "coaching-intervention-library.json"

VALID_BOTTLENECK_DIMS = {"C", "M", "E_exec", "E_env"}
VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}

PASS_COUNT = 0
FAIL_COUNT = 0
ERRORS: list[str] = []


def ok(msg: str) -> None:
    global PASS_COUNT
    PASS_COUNT += 1
    print(f"  ✅ {msg}")


def fail(msg: str) -> None:
    global FAIL_COUNT
    FAIL_COUNT += 1
    ERRORS.append(f"❌ {msg}")
    print(f"  ❌ {msg}")


def main() -> None:
    print("=" * 62)
    print("  教练干预手册验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not LIB_PATH.exists():
        fail(f"找不到文件: {LIB_PATH}")
        sys.exit(1)
    data = json.loads(LIB_PATH.read_text(encoding="utf-8"))
    ok("coaching-intervention-library.json 加载成功")

    interventions = data.get("interventions", [])
    ok(f"共 {len(interventions)} 条干预动作")

    # [2] 四维度全覆盖
    print("\n[2] 四维度干预条目覆盖")
    found_dims = {iv.get("bottleneck_dim") for iv in interventions}
    missing_dims = VALID_BOTTLENECK_DIMS - found_dims
    if missing_dims:
        fail(f"缺少维度干预: {missing_dims}")
    else:
        ok(f"四维度全覆盖 ✓ {sorted(found_dims)}")
    for dim in sorted(VALID_BOTTLENECK_DIMS):
        count = sum(1 for iv in interventions if iv.get("bottleneck_dim") == dim)
        if count >= 1:
            ok(f"  {dim}: {count}条干预动作 ✓")
        else:
            fail(f"  {dim}: 0条干预动作")

    # [3-8] 逐条验证
    print("\n[3-8] 逐条干预动作验证")
    dao_guard_iv_c05 = None
    for iv in interventions:
        ivid = iv.get("intervention_id", "?")
        dim = iv.get("bottleneck_dim", "?")
        label = ivid

        # [3] intervention_id 格式
        if re.match(r'^iv-[A-Za-z_]+-\d+$', ivid):
            ok(f"{label}: intervention_id 格式合规 ✓")
        else:
            fail(f"{label}: intervention_id='{ivid}' 格式不合规 (应为 iv-DIM-NN)")

        # dim 合规
        if dim in VALID_BOTTLENECK_DIMS:
            ok(f"{label}: bottleneck_dim='{dim}' 合规 ✓")
        else:
            fail(f"{label}: bottleneck_dim='{dim}' 非法")

        # [4] applicable_stages
        stages = iv.get("applicable_stages", [])
        if stages:
            invalid_stages = [s for s in stages if s not in range(1, 8)]
            if invalid_stages:
                fail(f"{label}: applicable_stages 含非法阶位 {invalid_stages}")
            else:
                ok(f"{label}: applicable_stages {stages} ∈ [1,7] ✓")
        else:
            fail(f"{label}: applicable_stages 为空")

        # [5] flywheel_support
        fw_support = iv.get("flywheel_support", [])
        if fw_support:
            invalid_fw = set(fw_support) - VALID_FLYWHEEL_NAMES
            if invalid_fw:
                fail(f"{label}: flywheel_support 含非法飞轮 {invalid_fw}")
            else:
                ok(f"{label}: flywheel_support {fw_support} 合规 ✓")
        else:
            fail(f"{label}: flywheel_support 为空")

        # [6] eight_step_ref
        esr = iv.get("eight_step_ref")
        if esr is not None:
            if 1 <= esr <= 8:
                ok(f"{label}: eight_step_ref={esr} ∈ [1,8] ✓")
            else:
                fail(f"{label}: eight_step_ref={esr} 超出 [1,8]")

        # [7] flywheel_ref
        fr = iv.get("flywheel_ref")
        if fr is not None:
            if 1 <= fr <= 6:
                ok(f"{label}: flywheel_ref={fr} ∈ [1,6] ✓")
            else:
                fail(f"{label}: flywheel_ref={fr} 超出 [1,6]")

        # required fields
        for req_f in ["primary_sop", "technique", "success_indicator"]:
            if iv.get(req_f):
                ok(f"{label}: {req_f} 存在 ✓")
            else:
                fail(f"{label}: {req_f} 缺失")

        # track iv-C-05
        if ivid == "iv-C-05":
            dao_guard_iv_c05 = iv

    # [8] ⑤守护
    print("\n[8] ⑤守护验证 (iv-C-05)")
    if dao_guard_iv_c05 is None:
        fail("iv-C-05 干预动作缺失")
    else:
        psop = dao_guard_iv_c05.get("primary_sop", "")
        guard = dao_guard_iv_c05.get("_dao_guard", "")
        if psop == "sop-05":
            ok("iv-C-05: primary_sop='sop-05' ✓")
        else:
            fail(f"iv-C-05: primary_sop='{psop}' ≠ 'sop-05'")
        if "_dao_guard" in dao_guard_iv_c05:
            ok("iv-C-05: _dao_guard 字段存在 ✓")
        else:
            fail("iv-C-05: 缺少 _dao_guard 字段")
        if "流程" in guard:
            ok("iv-C-05: _dao_guard 含'流程' ⑤联动守护 ✓")
        else:
            fail(f"iv-C-05: _dao_guard='{guard}' 未含'流程'")
        esr = dao_guard_iv_c05.get("eight_step_ref")
        if esr == 5:
            ok("iv-C-05: eight_step_ref=5 ✓")
        else:
            fail(f"iv-C-05: eight_step_ref={esr} ≠ 5")

    # [9] intervention_selection_guide
    print("\n[9] intervention_selection_guide")
    isg = data.get("intervention_selection_guide", {})
    if isg.get("stage_boundaries") and isg.get("flywheel_priority_by_stage"):
        ok("intervention_selection_guide stage_boundaries + flywheel_priority 存在 ✓")
    else:
        fail("intervention_selection_guide 缺少 stage_boundaries 或 flywheel_priority")

    fw_priority = isg.get("flywheel_priority_by_stage", {})
    for stage_key, fw_list in fw_priority.items():
        invalid_fw = set(fw_list) - VALID_FLYWHEEL_NAMES
        if invalid_fw:
            fail(f"flywheel_priority_by_stage.{stage_key} 含非法飞轮 {invalid_fw}")
        else:
            ok(f"flywheel_priority_by_stage.{stage_key}: {fw_list} 合规 ✓")

    # [10] validation_rules
    print("\n[10] validation_rules 合规")
    vr = data.get("validation_rules", {})
    step5_name = vr.get("eight_step_name_constraints", {}).get("step_id_5_name", "")
    if step5_name == "流程":
        ok("validation_rules step_id_5_name='流程' ⑤联动守护 ✓")
    else:
        fail(f"validation_rules step_id_5_name='{step5_name}' ≠ '流程'")

    fw_valid = set(vr.get("six_flywheel_valid_names", []))
    missing_fw_vr = VALID_FLYWHEEL_NAMES - fw_valid
    if missing_fw_vr:
        fail(f"six_flywheel_valid_names 缺少: {missing_fw_vr}")
    elif len(fw_valid) == 6:
        ok("six_flywheel_valid_names 六飞轮全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names 数量 {len(fw_valid)} ≠ 6")

    bk_enum = set(vr.get("bottleneck_dim_enum", []))
    if bk_enum == VALID_BOTTLENECK_DIMS:
        ok("bottleneck_dim_enum 四维度 ✓")
    else:
        fail(f"bottleneck_dim_enum 不匹配: {bk_enum}")

    # ── 结果 ──────────────────────────────────────────────────────
    print(f"\n{'=' * 62}")
    total = PASS_COUNT + FAIL_COUNT
    print(f"  结果: {PASS_COUNT}/{total} 通过 | {FAIL_COUNT} 失败")
    print("=" * 62)
    if FAIL_COUNT > 0:
        print("\n失败详情:")
        for e in ERRORS:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("  ✅ 教练干预手册验证 PASS — 全部干预动作合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
