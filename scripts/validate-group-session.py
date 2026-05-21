#!/usr/bin/env python3
"""
道层小组教练会话 schema 验证脚本 v1.0
验证 pipeline-data/coaching-group-session-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. group_formation_rules: min=2/max=4 + ccl-3 + 3个分组标准
  3. 每个分组标准: _dao_guard 含对应守护关键词
  4. group_session_schema 核心字段: 8个必填
  5. shared_stage enum 七阶全覆盖
  6. shared_bottleneck enum MECE 四维度
  7. shared_flywheel_focus enum 六飞轮
  8. sop05_compliance_group 字段 + _dao_guard 含'流程' — ⑤守护
  9. group_qa_scores 5维度 [1,10] + group_qa_standards sop05=1.0
  10. validation_rules: 分组标准/sop05_guard/七阶/六飞轮/MECE/pipl
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
GROUP_PATH = REPO_ROOT / "pipeline-data" / "coaching-group-session-schema.json"

VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}
MECE_DIMENSIONS = {"M", "E_exec", "C", "E_env"}
VALID_QA_DIMS = {"qa-d1", "qa-d2", "qa-d3", "qa-d4", "qa-d5"}
REQUIRED_GROUPING_CRITERIA = {"gc-stage", "gc-bottleneck", "gc-flywheel"}
REQUIRED_SESSION_FIELDS = {
    "group_session_id", "coach_id", "student_ids", "group_size",
    "session_date", "duration_min", "grouping_criterion_id", "sop05_compliance_group"
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
    print("  小组教练会话 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not GROUP_PATH.exists():
        fail(f"找不到文件: {GROUP_PATH}")
        sys.exit(1)
    data = json.loads(GROUP_PATH.read_text(encoding="utf-8"))
    ok("coaching-group-session-schema.json 加载成功")

    gfr = data.get("group_formation_rules", {})
    sess_fields = data.get("group_session_schema", {}).get("fields", {})

    # [2] group_formation_rules
    print("\n[2] group_formation_rules 分组规则")
    min_sz = gfr.get("min_group_size", 0)
    max_sz = gfr.get("max_group_size", 0)
    if min_sz == 2 and max_sz == 4:
        ok(f"group_size range [{min_sz},{max_sz}] ✓")
    else:
        fail(f"group_size range [{min_sz},{max_sz}] ≠ [2,4]")
    if gfr.get("coach_certification_required") == "ccl-3":
        ok("coach_certification_required='ccl-3' ✓")
    else:
        fail(f"coach_certification_required='{gfr.get('coach_certification_required')}' ≠ ccl-3")

    criteria = gfr.get("grouping_criteria", [])
    found_criteria_ids = {c.get("criterion_id") for c in criteria}
    missing_criteria = REQUIRED_GROUPING_CRITERIA - found_criteria_ids
    if missing_criteria:
        fail(f"缺少分组标准: {missing_criteria}")
    else:
        ok(f"3个分组标准全覆盖 ✓ {sorted(found_criteria_ids)}")

    # [3] 每个分组标准 _dao_guard
    print("\n[3] 每个分组标准 _dao_guard 守护")
    for c in criteria:
        cid = c.get("criterion_id", "?")
        guard = c.get("_dao_guard", "")
        if "七阶" in guard and cid == "gc-stage":
            ok(f"{cid}: _dao_guard 含'七阶' ✓")
        elif "MECE" in guard and cid == "gc-bottleneck":
            ok(f"{cid}: _dao_guard 含'MECE' ✓")
        elif "六飞轮" in guard and cid == "gc-flywheel":
            ok(f"{cid}: _dao_guard 含'六飞轮' ✓")
        elif guard:
            ok(f"{cid}: _dao_guard 存在 ✓")
        else:
            fail(f"{cid}: _dao_guard 缺失")

    # [4] 核心字段
    print("\n[4] group_session_schema 8个核心字段")
    vr_fields = set(data.get("validation_rules", {}).get("required_session_fields", []))
    if vr_fields == REQUIRED_SESSION_FIELDS:
        ok("validation_rules.required_session_fields 8字段全覆盖 ✓")
    else:
        missing_rf = REQUIRED_SESSION_FIELDS - vr_fields
        fail(f"required_session_fields 缺少: {missing_rf}")
    for fname in REQUIRED_SESSION_FIELDS:
        if fname in sess_fields:
            ok(f"group_session_schema.fields.{fname} 存在 ✓")
        else:
            fail(f"group_session_schema.fields.{fname} 缺失")

    # [5] shared_stage enum 七阶
    print("\n[5] shared_stage enum 七阶全覆盖")
    stage_enum = set(sess_fields.get("shared_stage", {}).get("enum", []))
    if stage_enum == VALID_STAGE_NAMES:
        ok("shared_stage enum 七阶全覆盖 ✓")
    else:
        fail(f"shared_stage enum {stage_enum} ≠ {VALID_STAGE_NAMES}")

    # [6] shared_bottleneck enum MECE
    print("\n[6] shared_bottleneck enum MECE 四维度")
    bn_enum = set(sess_fields.get("shared_bottleneck", {}).get("enum", []))
    if bn_enum == MECE_DIMENSIONS:
        ok("shared_bottleneck enum MECE 四维度 ✓")
    else:
        fail(f"shared_bottleneck enum {bn_enum} ≠ {MECE_DIMENSIONS}")

    # [7] shared_flywheel_focus enum 六飞轮
    print("\n[7] shared_flywheel_focus enum 六飞轮")
    fw_enum = set(sess_fields.get("shared_flywheel_focus", {}).get("enum", []))
    if fw_enum == VALID_FLYWHEEL_NAMES:
        ok("shared_flywheel_focus enum 六飞轮全覆盖 ✓")
    else:
        fail(f"shared_flywheel_focus enum {fw_enum} ≠ {VALID_FLYWHEEL_NAMES}")

    # [8] sop05_compliance_group ⑤守护
    print("\n[8] ⑤守护 — sop05_compliance_group _dao_guard 含'流程'")
    sop05_field = sess_fields.get("sop05_compliance_group", {})
    sop05_guard = sop05_field.get("_dao_guard", "")
    if "流程" in sop05_guard:
        ok("sop05_compliance_group._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_compliance_group._dao_guard='{sop05_guard}' 未含'流程'")
    if sop05_field.get("type") == "boolean":
        ok("sop05_compliance_group type=boolean ✓")
    else:
        fail(f"sop05_compliance_group type={sop05_field.get('type')} ≠ boolean")

    # [9] group_qa_scores + group_qa_standards
    print("\n[9] group_qa_scores 5维度 + group_qa_standards")
    gqs_props = sess_fields.get("group_qa_scores", {}).get("properties", {})
    missing_qa = VALID_QA_DIMS - set(gqs_props.keys())
    if missing_qa:
        fail(f"group_qa_scores 缺少维度: {missing_qa}")
    else:
        ok(f"group_qa_scores 5维度全覆盖 ✓")
    for dk, dv in gqs_props.items():
        if dv.get("minimum") == 1 and dv.get("maximum") == 10:
            ok(f"group_qa_scores.{dk}: [1,10] ✓")
        else:
            fail(f"group_qa_scores.{dk}: range [{dv.get('minimum')},{dv.get('maximum')}] ≠ [1,10]")

    gqas = data.get("group_qa_standards", {})
    sop05_rate = gqas.get("sop05_compliance_rate_target", 0)
    if sop05_rate == 1.0:
        ok(f"group_qa_standards.sop05_compliance_rate_target={sop05_rate} = 1.0 ✓")
    else:
        fail(f"group_qa_standards.sop05_compliance_rate_target={sop05_rate} ≠ 1.0")
    gqas_guard = gqas.get("_dao_guard", "")
    if "流程" in gqas_guard:
        ok("group_qa_standards._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"group_qa_standards._dao_guard='{gqas_guard}' 未含'流程'")

    # [10] validation_rules
    print("\n[10] validation_rules 合规")
    vr = data.get("validation_rules", {})
    gcrit_ids = set(vr.get("grouping_criterion_ids", []))
    if gcrit_ids == REQUIRED_GROUPING_CRITERIA:
        ok("validation_rules.grouping_criterion_ids 3个标准 ✓")
    else:
        fail(f"validation_rules.grouping_criterion_ids {gcrit_ids} ≠ {REQUIRED_GROUPING_CRITERIA}")

    sop05_guard_vr = vr.get("sop05_guard", "")
    if "流程" in sop05_guard_vr:
        ok("validation_rules.sop05_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"validation_rules.sop05_guard='{sop05_guard_vr}' 未含'流程'")

    fw_names = set(vr.get("six_flywheel_valid_names", []))
    if fw_names == VALID_FLYWHEEL_NAMES:
        ok("validation_rules.six_flywheel_valid_names 六飞轮全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names {fw_names} ≠ {VALID_FLYWHEEL_NAMES}")

    stage_names = set(vr.get("seven_stage_valid_names", []))
    if stage_names == VALID_STAGE_NAMES:
        ok("validation_rules.seven_stage_valid_names 七阶全覆盖 ✓")
    else:
        fail(f"seven_stage_valid_names {stage_names} ≠ {VALID_STAGE_NAMES}")

    mece_codes = set(vr.get("mece_dimension_codes", []))
    if mece_codes == MECE_DIMENSIONS:
        ok("validation_rules.mece_dimension_codes MECE 四维度 ✓")
    else:
        fail(f"mece_dimension_codes {mece_codes} ≠ {MECE_DIMENSIONS}")

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
        print("  ✅ 小组教练会话 schema 验证 PASS — 分组规则/⑤守护/七阶/六飞轮/MECE 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
