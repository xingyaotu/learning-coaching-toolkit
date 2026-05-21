#!/usr/bin/env python3
"""
道层教练会话笔记 schema 验证脚本 v1.0
验证 pipeline-data/coaching-session-notes-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. session_notes_schema 10个必填字段
  3. sop05_compliance ⑤守护 — type=boolean + _dao_guard 含'流程'
  4. current_stage_observation enum 七阶 + _dao_guard
  5. flywheel_focus_this_session enum 六飞轮 + _dao_guard
  6. next_session_plan 含六飞轮/七阶 enum
  7. notes_quality_standards _dao_guard 含'流程'/'七阶'/'六飞轮'
  8. note_templates 3组 + 每组 _dao_guard 含⑤守护
  9. privacy_boundaries 含 _dao_guard
  10. validation_rules: sop05_guard/七阶/六飞轮/MECE/pipl
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
NOTES_PATH = REPO_ROOT / "pipeline-data" / "coaching-session-notes-schema.json"

VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}
MECE_DIMENSIONS = {"M", "E_exec", "C", "E_env"}
REQUIRED_NOTE_FIELDS = {
    "note_id", "session_id", "student_id", "coach_id", "session_date",
    "session_type", "sop_id_used", "sop05_compliance",
    "current_stage_observation", "flywheel_focus_this_session"
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
    print("  教练会话笔记 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not NOTES_PATH.exists():
        fail(f"找不到文件: {NOTES_PATH}")
        sys.exit(1)
    data = json.loads(NOTES_PATH.read_text(encoding="utf-8"))
    ok("coaching-session-notes-schema.json 加载成功")

    fields = data.get("session_notes_schema", {}).get("fields", {})
    nqs = data.get("notes_quality_standards", {})
    templates = data.get("note_templates", {}).get("templates", [])
    pb = data.get("privacy_boundaries", {})
    vr = data.get("validation_rules", {})

    # [2] session_notes_schema 10个必填字段
    print("\n[2] session_notes_schema 10个必填字段")
    vr_req = set(vr.get("required_note_fields", []))
    if vr_req == REQUIRED_NOTE_FIELDS:
        ok("validation_rules.required_note_fields 10字段全覆盖 ✓")
    else:
        missing_rf = REQUIRED_NOTE_FIELDS - vr_req
        fail(f"required_note_fields 缺少: {missing_rf}")
    for fname in REQUIRED_NOTE_FIELDS:
        if fname in fields:
            ok(f"session_notes_schema.fields.{fname} 存在 ✓")
        else:
            fail(f"session_notes_schema.fields.{fname} 缺失")

    # [3] sop05_compliance ⑤守护
    print("\n[3] sop05_compliance ⑤守护")
    sop_field = fields.get("sop05_compliance", {})
    sop_guard = sop_field.get("_dao_guard", "")
    if "流程" in sop_guard:
        ok("sop05_compliance._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_compliance._dao_guard='{sop_guard}' 未含'流程'")
    if sop_field.get("type") == "boolean":
        ok("sop05_compliance type=boolean ✓")
    else:
        fail(f"sop05_compliance type={sop_field.get('type')} ≠ boolean")

    # [4] current_stage_observation enum 七阶 + _dao_guard
    print("\n[4] current_stage_observation enum 七阶 + _dao_guard")
    stage_field = fields.get("current_stage_observation", {})
    stage_enum = set(stage_field.get("enum", []))
    if stage_enum == VALID_STAGE_NAMES:
        ok("current_stage_observation enum 七阶全覆盖 ✓")
    else:
        fail(f"current_stage_observation enum {stage_enum} ≠ {VALID_STAGE_NAMES}")
    stage_guard = stage_field.get("_dao_guard", "")
    if "七阶" in stage_guard:
        ok("current_stage_observation._dao_guard 含'七阶' ✓")
    else:
        fail(f"current_stage_observation._dao_guard='{stage_guard}' 未含'七阶'")

    # [5] flywheel_focus_this_session enum 六飞轮 + _dao_guard
    print("\n[5] flywheel_focus_this_session enum 六飞轮 + _dao_guard")
    fw_field = fields.get("flywheel_focus_this_session", {})
    fw_enum = set(fw_field.get("enum", []))
    if fw_enum == VALID_FLYWHEEL_NAMES:
        ok("flywheel_focus_this_session enum 六飞轮全覆盖 ✓")
    else:
        fail(f"flywheel_focus_this_session enum {fw_enum} ≠ {VALID_FLYWHEEL_NAMES}")
    fw_guard = fw_field.get("_dao_guard", "")
    if "六飞轮" in fw_guard:
        ok("flywheel_focus_this_session._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"flywheel_focus_this_session._dao_guard='{fw_guard}' 未含'六飞轮'")

    # [6] next_session_plan 含六飞轮/七阶
    print("\n[6] next_session_plan 六飞轮/七阶 enum")
    nsp = fields.get("next_session_plan", {}).get("properties", {})
    nsp_fw = set(nsp.get("planned_flywheel_focus", {}).get("enum", []))
    if nsp_fw == VALID_FLYWHEEL_NAMES:
        ok("next_session_plan.planned_flywheel_focus enum 六飞轮全覆盖 ✓")
    else:
        fail(f"planned_flywheel_focus enum {nsp_fw} ≠ {VALID_FLYWHEEL_NAMES}")
    nsp_fw_guard = nsp.get("planned_flywheel_focus", {}).get("_dao_guard", "")
    if "六飞轮" in nsp_fw_guard:
        ok("planned_flywheel_focus._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"planned_flywheel_focus._dao_guard='{nsp_fw_guard}' 未含'六飞轮'")
    nsp_stage = set(nsp.get("planned_stage_target", {}).get("enum", []))
    if nsp_stage == VALID_STAGE_NAMES:
        ok("next_session_plan.planned_stage_target enum 七阶全覆盖 ✓")
    else:
        fail(f"planned_stage_target enum {nsp_stage} ≠ {VALID_STAGE_NAMES}")

    # [7] notes_quality_standards _dao_guard
    print("\n[7] notes_quality_standards _dao_guard 含'流程'/'七阶'/'六飞轮'")
    nqs_guard = nqs.get("_dao_guard", "")
    for kw in ["流程", "七阶", "六飞轮"]:
        if kw in nqs_guard:
            ok(f"notes_quality_standards._dao_guard 含'{kw}' ✓")
        else:
            fail(f"notes_quality_standards._dao_guard='{nqs_guard}' 未含'{kw}'")

    # [8] note_templates 3组 + ⑤守护
    print("\n[8] note_templates 3组 + ⑤守护")
    if len(templates) >= 3:
        ok(f"note_templates {len(templates)}组 ≥ 3 ✓")
    else:
        fail(f"note_templates {len(templates)} < 3")
    for t in templates:
        sg = t.get("stage_group", "?")
        t_guard = t.get("_dao_guard", "")
        sop_prompt = t.get("sop05_prompt", "")
        if "流程" in (t_guard + sop_prompt):
            ok(f"template '{sg}': 含'流程' ⑤守护 ✓")
        else:
            fail(f"template '{sg}': _dao_guard/sop05_prompt 未含'流程'")

    # [9] privacy_boundaries _dao_guard
    print("\n[9] privacy_boundaries _dao_guard")
    pb_guard = pb.get("_dao_guard", "")
    if "PIPL" in pb_guard and "六飞轮" in pb_guard:
        ok("privacy_boundaries._dao_guard 含'PIPL'+'六飞轮' ✓")
    else:
        fail(f"privacy_boundaries._dao_guard='{pb_guard}' 未含'PIPL'或'六飞轮'")

    # [10] validation_rules
    print("\n[10] validation_rules 合规")
    sop05_guard = vr.get("sop05_guard", "")
    if "流程" in sop05_guard:
        ok("validation_rules.sop05_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"validation_rules.sop05_guard='{sop05_guard}' 未含'流程'")
    stage_vr = set(vr.get("seven_stage_valid_names", []))
    if stage_vr == VALID_STAGE_NAMES:
        ok("validation_rules.seven_stage_valid_names 七阶全覆盖 ✓")
    else:
        fail(f"seven_stage_valid_names {stage_vr} ≠ {VALID_STAGE_NAMES}")
    fw_vr = set(vr.get("six_flywheel_valid_names", []))
    if fw_vr == VALID_FLYWHEEL_NAMES:
        ok("validation_rules.six_flywheel_valid_names 六飞轮全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names {fw_vr} ≠ {VALID_FLYWHEEL_NAMES}")
    mece_vr = set(vr.get("mece_dimension_codes", []))
    if mece_vr == MECE_DIMENSIONS:
        ok("validation_rules.mece_dimension_codes MECE 四维度 ✓")
    else:
        fail(f"mece_dimension_codes {mece_vr} ≠ {MECE_DIMENSIONS}")
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
        print("  ✅ 教练会话笔记 schema 验证 PASS — 笔记字段/⑤守护/七阶/六飞轮/MECE/PIPL 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
