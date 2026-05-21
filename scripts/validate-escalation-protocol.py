#!/usr/bin/env python3
"""
道层教练升级处置协议验证脚本 v1.0
验证 pipeline-data/coaching-escalation-protocol-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. escalation_levels: 5个等级全覆盖 + severity 1-5 递增
  3. 每个等级: trigger_conditions/protocol_steps/timeline_hours 非空
  4. esc-L3 触发条件含 '流程' — ⑤守护
  5. esc-L5 timeline_hours == 6 (紧急)
  6. escalation_record_schema 核心字段完整 + level_id enum 5个
  7. validation_rules: escalation_levels_count=5 + sop05_compliance_guard 含'流程'
  8. six_flywheel_valid_names 6个 + seven_stage_valid_names 7个
  9. PIPL 合规声明
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
ESCALATION_PATH = REPO_ROOT / "pipeline-data" / "coaching-escalation-protocol-schema.json"

REQUIRED_LEVEL_IDS = {"esc-L1", "esc-L2", "esc-L3", "esc-L4", "esc-L5"}
VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}

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
    print("  教练升级处置协议验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not ESCALATION_PATH.exists():
        fail(f"找不到文件: {ESCALATION_PATH}")
        sys.exit(1)
    data = json.loads(ESCALATION_PATH.read_text(encoding="utf-8"))
    ok("coaching-escalation-protocol-schema.json 加载成功")

    levels = data.get("escalation_levels", [])

    # [2] 5个等级 + severity 1-5 递增
    print("\n[2] escalation_levels 5等级 + severity 递增")
    found_ids = {lv.get("level_id") for lv in levels}
    missing = REQUIRED_LEVEL_IDS - found_ids
    if missing:
        fail(f"缺少升级等级: {missing}")
    else:
        ok(f"5个升级等级全覆盖 ✓ {sorted(found_ids)}")

    severities = [lv.get("severity", 0) for lv in sorted(levels, key=lambda x: x.get("level_id", ""))]
    if severities == sorted(severities) and len(set(severities)) == len(severities):
        ok(f"severity 递增 {severities} ✓")
    else:
        fail(f"severity 非严格递增: {severities}")

    # [3] 每个等级字段完整性
    print("\n[3] 每个等级字段完整性")
    for lv in levels:
        lid = lv.get("level_id", "?")
        tc = lv.get("trigger_conditions", [])
        ps = lv.get("protocol_steps", [])
        tl = lv.get("timeline_hours", 0)
        rd = lv.get("required_documentation", [])
        if tc:
            ok(f"{lid}: trigger_conditions {len(tc)}条 ✓")
        else:
            fail(f"{lid}: trigger_conditions 为空")
        if ps:
            ok(f"{lid}: protocol_steps {len(ps)}条 ✓")
        else:
            fail(f"{lid}: protocol_steps 为空")
        if tl > 0:
            ok(f"{lid}: timeline_hours={tl} > 0 ✓")
        else:
            fail(f"{lid}: timeline_hours={tl} ≤ 0")
        if rd:
            ok(f"{lid}: required_documentation {len(rd)}项 ✓")
        else:
            fail(f"{lid}: required_documentation 为空")

    # [4] esc-L3 触发条件含 '流程' — ⑤守护
    print("\n[4] ⑤守护 — esc-L3 触发条件含'流程'")
    l3 = next((lv for lv in levels if lv.get("level_id") == "esc-L3"), None)
    if l3 is None:
        fail("esc-L3 等级缺失")
    else:
        tc_text = str(l3.get("trigger_conditions", []))
        if "流程" in tc_text:
            ok("esc-L3 trigger_conditions 含'流程' ⑤守护 ✓")
        else:
            fail(f"esc-L3 trigger_conditions 未含'流程': {tc_text[:100]}")
        guard = l3.get("_dao_guard", "")
        if "流程" in guard:
            ok("esc-L3 _dao_guard 含'流程' ✓")
        else:
            fail(f"esc-L3 _dao_guard='{guard}' 未含'流程'")

    # [5] esc-L5 timeline_hours == 6 (紧急)
    print("\n[5] esc-L5 紧急响应时效")
    l5 = next((lv for lv in levels if lv.get("level_id") == "esc-L5"), None)
    if l5 is None:
        fail("esc-L5 等级缺失")
    else:
        tl5 = l5.get("timeline_hours", 0)
        if tl5 == 6:
            ok(f"esc-L5 timeline_hours={tl5}h (紧急) ✓")
        else:
            fail(f"esc-L5 timeline_hours={tl5} ≠ 6 (应为紧急6小时)")
        guard5 = l5.get("_dao_guard", "")
        if "PIPL" in guard5 or "匿名" in guard5:
            ok("esc-L5 _dao_guard 含 PIPL/匿名 ✓")
        else:
            fail(f"esc-L5 _dao_guard='{guard5}' 未提及 PIPL/匿名")

    # [6] escalation_record_schema 核心字段
    print("\n[6] escalation_record_schema 核心字段")
    rec_schema = data.get("documentation_standards", {}).get("escalation_record_schema", {})
    required_rec_fields = {"escalation_id", "student_id", "coach_id", "level_id",
                           "trigger_category", "trigger_description", "escalated_at", "outcome"}
    missing_rf = required_rec_fields - set(rec_schema.keys())
    if missing_rf:
        fail(f"escalation_record_schema 缺少字段: {missing_rf}")
    else:
        ok(f"escalation_record_schema {len(rec_schema)}个字段 核心字段全覆盖 ✓")

    level_enum = set(rec_schema.get("level_id", {}).get("enum", []))
    if level_enum == REQUIRED_LEVEL_IDS:
        ok("level_id enum 5个等级全覆盖 ✓")
    else:
        fail(f"level_id enum {level_enum} ≠ {REQUIRED_LEVEL_IDS}")

    outcome_enum = set(rec_schema.get("outcome", {}).get("enum", []))
    if outcome_enum:
        ok(f"outcome enum {len(outcome_enum)}个选项 ✓")
    else:
        fail("outcome enum 为空")

    # [7] validation_rules 合规
    print("\n[7] validation_rules 合规")
    vr = data.get("validation_rules", {})
    lc = vr.get("escalation_levels_count", 0)
    if lc == 5:
        ok("validation_rules.escalation_levels_count=5 ✓")
    else:
        fail(f"validation_rules.escalation_levels_count={lc} ≠ 5")

    guard_vr = vr.get("sop05_compliance_guard", "")
    if "流程" in guard_vr:
        ok("validation_rules.sop05_compliance_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"validation_rules.sop05_compliance_guard='{guard_vr}' 未含'流程'")

    tc_vr = vr.get("timeline_constraints", {})
    if tc_vr.get("esc-L5"):
        ok(f"timeline_constraints.esc-L5='{tc_vr['esc-L5']}' ✓")
    else:
        fail("timeline_constraints.esc-L5 缺失")

    # [8] 六飞轮 + 七阶
    print("\n[8] 六飞轮 + 七阶名称守护")
    fw_names = set(vr.get("six_flywheel_valid_names", []))
    missing_fw = VALID_FLYWHEEL_NAMES - fw_names
    if missing_fw:
        fail(f"six_flywheel_valid_names 缺少: {missing_fw}")
    elif len(fw_names) == 6:
        ok("validation_rules.six_flywheel_valid_names 六飞轮全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names 数量 {len(fw_names)} ≠ 6")

    stage_names = set(vr.get("seven_stage_valid_names", []))
    missing_st = VALID_STAGE_NAMES - stage_names
    if missing_st:
        fail(f"seven_stage_valid_names 缺少: {missing_st}")
    elif len(stage_names) == 7:
        ok("validation_rules.seven_stage_valid_names 七阶全覆盖 ✓")
    else:
        fail(f"seven_stage_valid_names 数量 {len(stage_names)} ≠ 7")

    # [9] PIPL 合规
    print("\n[9] PIPL 合规")
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
    anon_rule = data.get("documentation_standards", {}).get("anonymization_rule", "")
    if "匿名" in anon_rule or "PIPL" in anon_rule:
        ok("documentation_standards.anonymization_rule 存在 ✓")
    else:
        fail("documentation_standards.anonymization_rule 缺失")

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
        print("  ✅ 教练升级处置协议验证 PASS — 5等级升级协议全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
