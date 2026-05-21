#!/usr/bin/env python3
"""
道层教练入学流程 schema 验证脚本 v1.0
验证 pipeline-data/coaching-onboarding-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. onboarding_stages: 6阶段全覆盖 (sequence 1-6)
  3. 每阶段 required_inputs + outputs 非空
  4. ob-03 assessment_order 最高优先级为 assess_mece_capability
  5. ob-05 five_step_guard 含'流程' ⑤守护
  6. onboarding_checklist 核心检查项存在
  7. data_flow_summary input_schemas + output_schemas 非空
  8. validation_rules step_id_5_name='流程' + six_flywheel_valid_names 6个
  9. PIPL 合规声明多层存在
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
ONBOARD_PATH = REPO_ROOT / "pipeline-data" / "coaching-onboarding-schema.json"

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
    print("  教练入学流程 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not ONBOARD_PATH.exists():
        fail(f"找不到文件: {ONBOARD_PATH}")
        sys.exit(1)
    data = json.loads(ONBOARD_PATH.read_text(encoding="utf-8"))
    ok("coaching-onboarding-schema.json 加载成功")

    stages = data.get("onboarding_stages", [])

    # [2] 6阶段全覆盖
    print("\n[2] onboarding_stages 6阶段全覆盖")
    found_seqs = {s.get("sequence") for s in stages}
    missing_seqs = set(range(1, 7)) - found_seqs
    if missing_seqs:
        fail(f"缺少 sequence: {missing_seqs}")
    elif len(stages) == 6:
        ok(f"6阶段全覆盖 ✓ (sequence 1-6)")
    else:
        fail(f"阶段数量 {len(stages)} ≠ 6")

    # [3-5] 逐阶段验证
    print("\n[3-5] 逐阶段验证")
    ob05 = None
    ob03 = None
    for s in sorted(stages, key=lambda x: x.get("sequence", 0)):
        sid = s.get("stage_id", "?")
        sname = s.get("stage_name", "?")
        label = f"{sid}({sname})"

        # [3] required_inputs + outputs 非空
        ri = s.get("required_inputs", [])
        op = s.get("outputs", [])
        if ri:
            ok(f"{label}: required_inputs {len(ri)}个 ✓")
        else:
            fail(f"{label}: required_inputs 为空")
        if op:
            ok(f"{label}: outputs {len(op)}个 ✓")
        else:
            fail(f"{label}: outputs 为空")

        # duration_estimate_min
        dur = s.get("duration_estimate_min", 0)
        if dur > 0:
            ok(f"{label}: duration_estimate_min={dur}分 ✓")
        else:
            fail(f"{label}: duration_estimate_min 缺失或 ≤ 0")

        if sid == "ob-03":
            ob03 = s
        if sid == "ob-05":
            ob05 = s

    # [4] ob-03 assessment_order 最高优先级
    print("\n[4] ob-03 assessment_order 验证")
    if ob03 is None:
        fail("ob-03 阶段缺失")
    else:
        ao = ob03.get("assessment_order", [])
        if ao:
            priority1 = next((a for a in ao if a.get("priority") == 1), None)
            if priority1 and priority1.get("tool") == "assess_mece_capability":
                ok("ob-03: priority=1 tool='assess_mece_capability' ✓")
            else:
                fail(f"ob-03: priority=1 tool='{priority1.get('tool') if priority1 else None}' ≠ 'assess_mece_capability'")
            ok(f"ob-03: assessment_order {len(ao)}个优先级 ✓")
        else:
            fail("ob-03: assessment_order 为空")

    # [5] ob-05 ⑤守护
    print("\n[5] ⑤守护验证 (ob-05)")
    if ob05 is None:
        fail("ob-05 阶段缺失")
    else:
        five_guard = ob05.get("eight_step_initial_focus", {}).get("five_step_guard", "")
        if "流程" in five_guard and "sop-05" in five_guard:
            ok(f"ob-05: five_step_guard 含'流程'+'sop-05' ⑤守护 ✓")
        elif "流程" in five_guard:
            ok(f"ob-05: five_step_guard 含'流程' ⑤守护 ✓")
        else:
            fail(f"ob-05: five_step_guard='{five_guard}' 未含'流程'")

        # flywheel_initial_focus fallback
        fw_fallback = ob05.get("flywheel_initial_focus", {}).get("fallback", [])
        if fw_fallback:
            invalid_fw = set(fw_fallback) - VALID_FLYWHEEL_NAMES
            if invalid_fw:
                fail(f"ob-05: flywheel_initial_focus.fallback 含非法飞轮 {invalid_fw}")
            else:
                ok(f"ob-05: flywheel_initial_focus.fallback {fw_fallback} 合规 ✓")
        else:
            fail("ob-05: flywheel_initial_focus.fallback 为空")

    # [6] onboarding_checklist
    print("\n[6] onboarding_checklist 验证")
    checklist = data.get("onboarding_checklist", {})
    required_completions = checklist.get("required_completions", [])
    if len(required_completions) >= 6:
        ok(f"required_completions {len(required_completions)}项 ≥ 6 ✓")
    else:
        fail(f"required_completions 仅 {len(required_completions)} 项 < 6")

    pipl_checklist = checklist.get("pipl_checklist", [])
    if len(pipl_checklist) >= 3:
        ok(f"pipl_checklist {len(pipl_checklist)}项 ✓")
    else:
        fail(f"pipl_checklist 仅 {len(pipl_checklist)} 项 < 3")

    # Check flywheel mention in checklist
    checklist_text = str(required_completions)
    if "六飞轮" in checklist_text or any("飞轮" in item for item in required_completions):
        ok("checklist 包含六飞轮检查项 ✓")
    else:
        fail("checklist 缺少六飞轮检查项")

    # [7] data_flow_summary
    print("\n[7] data_flow_summary 验证")
    dfs = data.get("data_flow_summary", {})
    input_schemas = dfs.get("input_schemas", [])
    output_schemas = dfs.get("output_schemas", [])
    if len(input_schemas) >= 5:
        ok(f"input_schemas {len(input_schemas)}个 ✓")
    else:
        fail(f"input_schemas 仅 {len(input_schemas)} 个 < 5")
    if len(output_schemas) >= 2:
        ok(f"output_schemas {len(output_schemas)}个 ✓")
    else:
        fail(f"output_schemas 仅 {len(output_schemas)} 个 < 2")

    # [8] validation_rules
    print("\n[8] validation_rules 合规")
    vr = data.get("validation_rules", {})
    step5_name = vr.get("eight_step_name_constraints", {}).get("step_id_5_name", "")
    if step5_name == "流程":
        ok("validation_rules step_id_5_name='流程' ⑤联动守护 ✓")
    else:
        fail(f"validation_rules step_id_5_name='{step5_name}' ≠ '流程'")

    fw_valid = set(vr.get("six_flywheel_valid_names", []))
    missing_fw = VALID_FLYWHEEL_NAMES - fw_valid
    if missing_fw:
        fail(f"six_flywheel_valid_names 缺少: {missing_fw}")
    elif len(fw_valid) == 6:
        ok("six_flywheel_valid_names 六飞轮全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names 数量 {len(fw_valid)} ≠ 6")

    stage_count = vr.get("onboarding_stage_count", 0)
    if stage_count == 6:
        ok("validation_rules.onboarding_stage_count=6 ✓")
    else:
        fail(f"validation_rules.onboarding_stage_count={stage_count} ≠ 6")

    # [9] PIPL 多层检查
    print("\n[9] PIPL 合规多层验证")
    pipl_meta = data.get("_meta", {}).get("pipl_note", "")
    if "PIPL" in pipl_meta and "匿名" in pipl_meta:
        ok("_meta.pipl_note PIPL 合规声明 ✓")
    else:
        fail("_meta.pipl_note 缺少 PIPL 合规声明")

    pipl_vr = vr.get("pipl_constraints", "")
    if "PIPL" in pipl_vr or "匿名" in pipl_vr:
        ok("validation_rules.pipl_constraints 存在 ✓")
    else:
        fail("validation_rules.pipl_constraints 缺失")

    # ob-01 PIPL constraint
    ob01 = next((s for s in stages if s.get("stage_id") == "ob-01"), None)
    if ob01:
        pc = ob01.get("pipl_constraint", "")
        if "真实姓名" in pc or "联系方式" in pc:
            ok("ob-01: pipl_constraint 存在 ✓")
        else:
            fail(f"ob-01: pipl_constraint='{pc}' 缺少 PIPL 具体约束")

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
        print("  ✅ 教练入学流程 schema 验证 PASS — 6阶段全流程合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
