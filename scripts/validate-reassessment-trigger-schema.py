#!/usr/bin/env python3
"""
道层教练复测触发 schema 验证脚本 v1.0
验证 pipeline-data/coaching-reassessment-trigger-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. reassessment_signals: 5个信号 + 关键信号 _dao_guard
  3. ras-stage-jump 含'七阶'; ras-bottleneck-shift 含'MECE'; ras-flywheel-mastery 含'六飞轮'
  4. reassessment_request_schema 7个必填字段
  5. coach_observed_stage enum 七阶
  6. signal_id enum 5个信号
  7. coach_observed_primary_bottleneck enum MECE
  8. coach_observed_flywheel_progress enum 六飞轮 + _dao_guard
  9. sop05_compliance_last_session ⑤守护
  10. validation_rules: sop05_guard/七阶/MECE/六飞轮/pipl
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TRIGGER_PATH = REPO_ROOT / "pipeline-data" / "coaching-reassessment-trigger-schema.json"

VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}
MECE_DIMENSIONS = {"M", "E_exec", "C", "E_env"}
VALID_SIGNAL_IDS = {
    "ras-stage-jump", "ras-bottleneck-shift", "ras-flywheel-mastery",
    "ras-plan-milestone", "ras-regression"
}
REQUIRED_REQUEST_FIELDS = {
    "request_id", "student_id", "coach_id", "request_date",
    "signal_id", "coach_observed_stage", "request_status"
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
    print("  教练复测触发 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not TRIGGER_PATH.exists():
        fail(f"找不到文件: {TRIGGER_PATH}")
        sys.exit(1)
    data = json.loads(TRIGGER_PATH.read_text(encoding="utf-8"))
    ok("coaching-reassessment-trigger-schema.json 加载成功")

    signals = data.get("reassessment_signals", {}).get("signals", [])
    req_fields = data.get("reassessment_request_schema", {}).get("fields", {})
    vr = data.get("validation_rules", {})

    # [2] reassessment_signals 5个
    print("\n[2] reassessment_signals 5个信号")
    found_signals = {s.get("signal_id") for s in signals}
    missing_signals = VALID_SIGNAL_IDS - found_signals
    if missing_signals:
        fail(f"缺少信号: {missing_signals}")
    else:
        ok(f"5个复测信号全覆盖 ✓ {sorted(found_signals)}")

    # [3] 关键信号 _dao_guard
    print("\n[3] 关键信号 _dao_guard 含七阶/MECE/六飞轮")
    signal_map = {s.get("signal_id"): s for s in signals}
    jump = signal_map.get("ras-stage-jump", {})
    if "七阶" in jump.get("_dao_guard", ""):
        ok("ras-stage-jump._dao_guard 含'七阶' ✓")
    else:
        fail(f"ras-stage-jump._dao_guard='{jump.get('_dao_guard', '')}' 未含'七阶'")
    bottleneck = signal_map.get("ras-bottleneck-shift", {})
    if "MECE" in bottleneck.get("_dao_guard", ""):
        ok("ras-bottleneck-shift._dao_guard 含'MECE' ✓")
    else:
        fail(f"ras-bottleneck-shift._dao_guard='{bottleneck.get('_dao_guard', '')}' 未含'MECE'")
    flywheel = signal_map.get("ras-flywheel-mastery", {})
    if "六飞轮" in flywheel.get("_dao_guard", ""):
        ok("ras-flywheel-mastery._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"ras-flywheel-mastery._dao_guard='{flywheel.get('_dao_guard', '')}' 未含'六飞轮'")

    # [4] reassessment_request_schema 7个必填字段
    print("\n[4] reassessment_request_schema 7个必填字段")
    vr_req = set(vr.get("required_request_fields", []))
    if vr_req == REQUIRED_REQUEST_FIELDS:
        ok("validation_rules.required_request_fields 7字段全覆盖 ✓")
    else:
        missing_rf = REQUIRED_REQUEST_FIELDS - vr_req
        fail(f"required_request_fields 缺少: {missing_rf}")
    for fname in REQUIRED_REQUEST_FIELDS:
        if fname in req_fields:
            ok(f"reassessment_request_schema.fields.{fname} 存在 ✓")
        else:
            fail(f"reassessment_request_schema.fields.{fname} 缺失")

    # [5] coach_observed_stage enum 七阶
    print("\n[5] coach_observed_stage enum 七阶全覆盖")
    stage_enum = set(req_fields.get("coach_observed_stage", {}).get("enum", []))
    if stage_enum == VALID_STAGE_NAMES:
        ok("coach_observed_stage enum 七阶全覆盖 ✓")
    else:
        fail(f"coach_observed_stage enum {stage_enum} ≠ {VALID_STAGE_NAMES}")

    # [6] signal_id enum 5个
    print("\n[6] signal_id enum 5个信号")
    sig_enum = set(req_fields.get("signal_id", {}).get("enum", []))
    if sig_enum == VALID_SIGNAL_IDS:
        ok("signal_id enum 5个信号全覆盖 ✓")
    else:
        fail(f"signal_id enum {sig_enum} ≠ {VALID_SIGNAL_IDS}")

    # [7] coach_observed_primary_bottleneck enum MECE
    print("\n[7] coach_observed_primary_bottleneck enum MECE")
    bn_enum = set(req_fields.get("coach_observed_primary_bottleneck", {}).get("enum", []))
    if bn_enum == MECE_DIMENSIONS:
        ok("coach_observed_primary_bottleneck enum MECE 四维度 ✓")
    else:
        fail(f"coach_observed_primary_bottleneck enum {bn_enum} ≠ {MECE_DIMENSIONS}")

    # [8] coach_observed_flywheel_progress enum 六飞轮 + _dao_guard
    print("\n[8] coach_observed_flywheel_progress enum 六飞轮 + _dao_guard")
    fw_items = req_fields.get("coach_observed_flywheel_progress", {}).get("items", {})
    fw_enum = set(fw_items.get("enum", []))
    if fw_enum == VALID_FLYWHEEL_NAMES:
        ok("coach_observed_flywheel_progress enum 六飞轮全覆盖 ✓")
    else:
        fail(f"flywheel_progress enum {fw_enum} ≠ {VALID_FLYWHEEL_NAMES}")
    fw_guard = req_fields.get("coach_observed_flywheel_progress", {}).get("_dao_guard", "")
    if "六飞轮" in fw_guard:
        ok("coach_observed_flywheel_progress._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"coach_observed_flywheel_progress._dao_guard='{fw_guard}' 未含'六飞轮'")

    # [9] sop05_compliance_last_session ⑤守护
    print("\n[9] sop05_compliance_last_session ⑤守护")
    sop_field = req_fields.get("sop05_compliance_last_session", {})
    sop_guard = sop_field.get("_dao_guard", "")
    if "流程" in sop_guard:
        ok("sop05_compliance_last_session._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_compliance_last_session._dao_guard='{sop_guard}' 未含'流程'")

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
    mece_vr = set(vr.get("mece_dimension_codes", []))
    if mece_vr == MECE_DIMENSIONS:
        ok("validation_rules.mece_dimension_codes MECE 四维度 ✓")
    else:
        fail(f"mece_dimension_codes {mece_vr} ≠ {MECE_DIMENSIONS}")
    fw_vr = set(vr.get("six_flywheel_valid_names", []))
    if fw_vr == VALID_FLYWHEEL_NAMES:
        ok("validation_rules.six_flywheel_valid_names 六飞轮全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names {fw_vr} ≠ {VALID_FLYWHEEL_NAMES}")
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
        print("  ✅ 教练复测触发 schema 验证 PASS — 5信号/⑤守护/七阶/MECE/六飞轮/PIPL 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
