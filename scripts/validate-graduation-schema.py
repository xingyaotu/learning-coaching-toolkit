#!/usr/bin/env python3
"""
道层教练毕业/结案 schema 验证脚本 v1.0
验证 pipeline-data/coaching-graduation-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. graduation_criteria: 3种标准 + _dao_guard 含守护关键词
  3. graduation_process: 6步流程 + sop05_final_check 含'流程'
  4. graduation_record_schema 10个必填字段
  5. initial_stage/final_stage enum 七阶全覆盖
  6. graduation_criteria_id enum 3种标准
  7. primary_bottleneck_resolved enum MECE 四维度
  8. flywheel_completion_summary 六飞轮 + _dao_guard
  9. sop05_final_compliance ⑤守护
  10. validation_rules: sop05_guard/七阶/六飞轮/MECE/pipl
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
GRAD_PATH = REPO_ROOT / "pipeline-data" / "coaching-graduation-schema.json"

VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}
MECE_DIMENSIONS = {"M", "E_exec", "C", "E_env"}
VALID_CRITERIA_IDS = {"gc-standard", "gc-early", "gc-milestone"}
REQUIRED_RECORD_FIELDS = {
    "graduation_id", "student_id", "coach_id", "graduation_date",
    "graduation_criteria_id", "total_sessions_completed",
    "initial_stage", "final_stage", "sop05_final_compliance", "graduation_status"
}

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
    print("  教练毕业/结案 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not GRAD_PATH.exists():
        fail(f"找不到文件: {GRAD_PATH}")
        sys.exit(1)
    data = json.loads(GRAD_PATH.read_text(encoding="utf-8"))
    ok("coaching-graduation-schema.json 加载成功")

    gc = data.get("graduation_criteria", {})
    rec_fields = data.get("graduation_record_schema", {}).get("fields", {})

    # [2] graduation_criteria 3种标准 + _dao_guard
    print("\n[2] graduation_criteria 3种标准 + _dao_guard")
    found_criteria = {k for k in gc.keys() if not k.startswith("description")}
    criteria_objs = {k: gc[k] for k in found_criteria if isinstance(gc[k], dict)}
    criteria_ids = {v.get("criteria_id") for v in criteria_objs.values()}
    missing_criteria = VALID_CRITERIA_IDS - criteria_ids
    if missing_criteria:
        fail(f"缺少毕业标准: {missing_criteria}")
    else:
        ok(f"3种毕业标准全覆盖 ✓ {sorted(criteria_ids)}")
    for name, obj in criteria_objs.items():
        guard = obj.get("_dao_guard", "")
        if guard:
            ok(f"{name}: _dao_guard 存在 ✓")
        else:
            fail(f"{name}: _dao_guard 缺失")

    # [3] graduation_process 6步 + sop05_final_check 含'流程'
    print("\n[3] graduation_process 6步流程 + ⑤守护")
    gp = data.get("graduation_process", {})
    steps = gp.get("steps", [])
    if len(steps) >= 6:
        ok(f"graduation_process.steps {len(steps)}步 ≥ 6 ✓")
    else:
        fail(f"graduation_process.steps {len(steps)} < 6")
    sop_check = gp.get("sop05_final_check", {})
    sop_check_guard = sop_check.get("_dao_guard", "")
    if "流程" in sop_check_guard:
        ok("graduation_process.sop05_final_check._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"graduation_process.sop05_final_check._dao_guard='{sop_check_guard}' 未含'流程'")

    # [4] graduation_record_schema 10个必填字段
    print("\n[4] graduation_record_schema 10个必填字段")
    vr_req = set(data.get("validation_rules", {}).get("required_graduation_fields", []))
    if vr_req == REQUIRED_RECORD_FIELDS:
        ok("validation_rules.required_graduation_fields 10字段全覆盖 ✓")
    else:
        missing_rf = REQUIRED_RECORD_FIELDS - vr_req
        fail(f"required_graduation_fields 缺少: {missing_rf}")
    for fname in REQUIRED_RECORD_FIELDS:
        if fname in rec_fields:
            ok(f"graduation_record_schema.fields.{fname} 存在 ✓")
        else:
            fail(f"graduation_record_schema.fields.{fname} 缺失")

    # [5] initial_stage/final_stage enum 七阶
    print("\n[5] initial_stage/final_stage enum 七阶全覆盖")
    init_enum = set(rec_fields.get("initial_stage", {}).get("enum", []))
    final_enum = set(rec_fields.get("final_stage", {}).get("enum", []))
    if init_enum == VALID_STAGE_NAMES:
        ok("initial_stage enum 七阶全覆盖 ✓")
    else:
        fail(f"initial_stage enum {init_enum} ≠ {VALID_STAGE_NAMES}")
    if final_enum == VALID_STAGE_NAMES:
        ok("final_stage enum 七阶全覆盖 ✓")
    else:
        fail(f"final_stage enum {final_enum} ≠ {VALID_STAGE_NAMES}")

    # [6] graduation_criteria_id enum 3种
    print("\n[6] graduation_criteria_id enum 3种标准")
    crit_enum = set(rec_fields.get("graduation_criteria_id", {}).get("enum", []))
    if crit_enum == VALID_CRITERIA_IDS:
        ok("graduation_criteria_id enum 3种标准全覆盖 ✓")
    else:
        fail(f"graduation_criteria_id enum {crit_enum} ≠ {VALID_CRITERIA_IDS}")

    # [7] primary_bottleneck_resolved enum MECE
    print("\n[7] primary_bottleneck_resolved enum MECE 四维度")
    bn_enum = set(rec_fields.get("primary_bottleneck_resolved", {}).get("enum", []))
    if bn_enum == MECE_DIMENSIONS:
        ok("primary_bottleneck_resolved enum MECE 四维度 ✓")
    else:
        fail(f"primary_bottleneck_resolved enum {bn_enum} ≠ {MECE_DIMENSIONS}")

    # [8] flywheel_completion_summary 六飞轮 + _dao_guard
    print("\n[8] flywheel_completion_summary 六飞轮 + _dao_guard")
    fcs = rec_fields.get("flywheel_completion_summary", {})
    fcs_props = fcs.get("properties", {})
    fcs_keys = set(fcs_props.keys())
    if fcs_keys == VALID_FLYWHEEL_NAMES:
        ok("flywheel_completion_summary 六飞轮全覆盖 ✓")
    else:
        fail(f"flywheel_completion_summary 飞轮 {fcs_keys} ≠ {VALID_FLYWHEEL_NAMES}")
    fcs_guard = fcs.get("_dao_guard", "")
    if "六飞轮" in fcs_guard:
        ok("flywheel_completion_summary._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"flywheel_completion_summary._dao_guard='{fcs_guard}' 未含'六飞轮'")

    # [9] sop05_final_compliance ⑤守护
    print("\n[9] sop05_final_compliance ⑤守护")
    sop_field = rec_fields.get("sop05_final_compliance", {})
    sop_guard = sop_field.get("_dao_guard", "")
    if "流程" in sop_guard:
        ok("sop05_final_compliance._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_final_compliance._dao_guard='{sop_guard}' 未含'流程'")
    if sop_field.get("type") == "boolean":
        ok("sop05_final_compliance type=boolean ✓")
    else:
        fail(f"sop05_final_compliance type={sop_field.get('type')} ≠ boolean")

    # [10] validation_rules
    print("\n[10] validation_rules 合规")
    vr = data.get("validation_rules", {})
    sop05_guard_vr = vr.get("sop05_guard", "")
    if "流程" in sop05_guard_vr:
        ok("validation_rules.sop05_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"validation_rules.sop05_guard='{sop05_guard_vr}' 未含'流程'")
    stage_names = set(vr.get("valid_stage_enum", []))
    if stage_names == VALID_STAGE_NAMES:
        ok("validation_rules.valid_stage_enum 七阶全覆盖 ✓")
    else:
        fail(f"valid_stage_enum {stage_names} ≠ {VALID_STAGE_NAMES}")
    fw_names = set(vr.get("six_flywheel_valid_names", []))
    if fw_names == VALID_FLYWHEEL_NAMES:
        ok("validation_rules.six_flywheel_valid_names 六飞轮全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names {fw_names} ≠ {VALID_FLYWHEEL_NAMES}")
    mece_codes = set(vr.get("valid_mece_dimensions", []))
    if mece_codes == MECE_DIMENSIONS:
        ok("validation_rules.valid_mece_dimensions MECE 四维度 ✓")
    else:
        fail(f"valid_mece_dimensions {mece_codes} ≠ {MECE_DIMENSIONS}")
    pipl_meta = data.get("_meta", {}).get("pipl_note", "")
    if "PIPL" in pipl_meta and "匿名" in pipl_meta:
        ok("_meta.pipl_note PIPL 合规声明 ✓")
    else:
        fail("_meta.pipl_note 缺少 PIPL 合规声明")
    pipl_vr = vr.get("pipl_constraints", "")
    if "PIPL" in pipl_vr and "匿名" in pipl_vr:
        ok("validation_rules.pipl_constraints 存在 ✓")
    else:
        fail("validation_rules.pipl_constraints 缺失或不完整")

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
        print("  ✅ 教练毕业/结案 schema 验证 PASS — 毕业标准/⑤守护/七阶/六飞轮/MECE/PIPL 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
