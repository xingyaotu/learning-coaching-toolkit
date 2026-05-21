#!/usr/bin/env python3
"""
道层教练脱落风险预警 schema 验证脚本 v1.0
验证 pipeline-data/coaching-dropout-risk-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. dropout_risk_indicators: 5个指标 + 权重和 = 1.0
  3. 学习进度指标 _dao_guard 含七阶/六飞轮
  4. risk_levels: 4个等级 + rl-critical 含_dao_guard
  5. intervention_strategies: 4种干预 + _dao_guard
  6. is-sop-adjust 含'流程' ⑤守护
  7. dropout_risk_record_schema 8个必填字段
  8. current_stage enum 七阶全覆盖
  9. risk_level_id enum 4个等级
  10. validation_rules: sop05_guard/七阶/六飞轮/MECE/权重和/pipl
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DROPOUT_PATH = REPO_ROOT / "pipeline-data" / "coaching-dropout-risk-schema.json"

VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}
MECE_DIMENSIONS = {"M", "E_exec", "C", "E_env"}
VALID_RISK_LEVELS = {"rl-low", "rl-medium", "rl-high", "rl-critical"}
VALID_INDICATOR_IDS = {"dri-miss", "dri-late", "dri-engagement", "dri-stage-stall", "dri-flywheel-decline"}
VALID_STRATEGY_IDS = {"is-sop-adjust", "is-flywheel-refocus", "is-stage-recalibrate", "is-escalate"}
REQUIRED_RISK_FIELDS = {
    "risk_record_id", "student_id", "coach_id", "assessment_date",
    "risk_level_id", "composite_risk_score", "triggered_indicators", "current_stage"
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
    print("  教练脱落风险预警 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not DROPOUT_PATH.exists():
        fail(f"找不到文件: {DROPOUT_PATH}")
        sys.exit(1)
    data = json.loads(DROPOUT_PATH.read_text(encoding="utf-8"))
    ok("coaching-dropout-risk-schema.json 加载成功")

    dri = data.get("dropout_risk_indicators", {})
    risk_levels = data.get("risk_levels", {}).get("levels", [])
    strategies = data.get("intervention_strategies", {}).get("strategies", [])
    rec_fields = data.get("dropout_risk_record_schema", {}).get("fields", {})
    vr = data.get("validation_rules", {})

    # [2] dropout_risk_indicators 5个指标 + 权重和
    print("\n[2] dropout_risk_indicators 5个指标 + 权重和 = 1.0")
    session_inds = dri.get("session_behavior_indicators", [])
    progress_inds = dri.get("learning_progress_indicators", [])
    all_inds = session_inds + progress_inds
    found_ind_ids = {i.get("indicator_id") for i in all_inds}
    missing_inds = VALID_INDICATOR_IDS - found_ind_ids
    if missing_inds:
        fail(f"缺少指标: {missing_inds}")
    else:
        ok(f"5个风险指标全覆盖 ✓ {sorted(found_ind_ids)}")
    total_weight = sum(i.get("weight", 0) for i in all_inds)
    if abs(total_weight - 1.0) < 1e-9:
        ok(f"指标权重和 = {total_weight:.2f} = 1.0 ✓")
    else:
        fail(f"指标权重和 = {total_weight:.2f} ≠ 1.0")

    # [3] 学习进度指标 _dao_guard
    print("\n[3] 学习进度指标 _dao_guard 含七阶/六飞轮")
    for ind in progress_inds:
        iid = ind.get("indicator_id", "?")
        guard = ind.get("_dao_guard", "")
        if iid == "dri-stage-stall" and "七阶" in guard:
            ok(f"{iid}: _dao_guard 含'七阶' ✓")
        elif iid == "dri-flywheel-decline" and "六飞轮" in guard:
            ok(f"{iid}: _dao_guard 含'六飞轮' ✓")
        elif guard:
            ok(f"{iid}: _dao_guard 存在 ✓")
        else:
            fail(f"{iid}: _dao_guard 缺失")

    # [4] risk_levels 4个等级 + rl-critical _dao_guard
    print("\n[4] risk_levels 4个等级 + rl-critical _dao_guard")
    found_levels = {l.get("level_id") for l in risk_levels}
    missing_levels = VALID_RISK_LEVELS - found_levels
    if missing_levels:
        fail(f"缺少风险等级: {missing_levels}")
    else:
        ok(f"4个风险等级全覆盖 ✓ {sorted(found_levels)}")
    critical = next((l for l in risk_levels if l.get("level_id") == "rl-critical"), None)
    if critical and critical.get("_dao_guard"):
        ok("rl-critical._dao_guard 存在 ✓")
    else:
        fail("rl-critical._dao_guard 缺失")

    # [5] intervention_strategies 4种
    print("\n[5] intervention_strategies 4种干预 + _dao_guard")
    found_strategy_ids = {s.get("strategy_id") for s in strategies}
    missing_strategies = VALID_STRATEGY_IDS - found_strategy_ids
    if missing_strategies:
        fail(f"缺少干预策略: {missing_strategies}")
    else:
        ok(f"4种干预策略全覆盖 ✓ {sorted(found_strategy_ids)}")
    for s in strategies:
        sid = s.get("strategy_id", "?")
        guard = s.get("_dao_guard", "")
        if guard:
            ok(f"{sid}: _dao_guard 存在 ✓")
        else:
            fail(f"{sid}: _dao_guard 缺失")

    # [6] is-sop-adjust 含'流程' ⑤守护
    print("\n[6] is-sop-adjust ⑤守护 — _dao_guard 含'流程'")
    sop_strat = next((s for s in strategies if s.get("strategy_id") == "is-sop-adjust"), None)
    if sop_strat:
        sop_guard = sop_strat.get("_dao_guard", "")
        if "流程" in sop_guard:
            ok("is-sop-adjust._dao_guard 含'流程' ⑤守护 ✓")
        else:
            fail(f"is-sop-adjust._dao_guard='{sop_guard}' 未含'流程'")
    else:
        fail("is-sop-adjust 策略缺失")

    # [7] dropout_risk_record_schema 8个必填字段
    print("\n[7] dropout_risk_record_schema 8个必填字段")
    vr_req = set(vr.get("required_risk_fields", []))
    if vr_req == REQUIRED_RISK_FIELDS:
        ok("validation_rules.required_risk_fields 8字段全覆盖 ✓")
    else:
        missing_rf = REQUIRED_RISK_FIELDS - vr_req
        fail(f"required_risk_fields 缺少: {missing_rf}")
    for fname in REQUIRED_RISK_FIELDS:
        if fname in rec_fields:
            ok(f"dropout_risk_record_schema.fields.{fname} 存在 ✓")
        else:
            fail(f"dropout_risk_record_schema.fields.{fname} 缺失")

    # [8] current_stage enum 七阶
    print("\n[8] current_stage enum 七阶全覆盖")
    stage_enum = set(rec_fields.get("current_stage", {}).get("enum", []))
    if stage_enum == VALID_STAGE_NAMES:
        ok("current_stage enum 七阶全覆盖 ✓")
    else:
        fail(f"current_stage enum {stage_enum} ≠ {VALID_STAGE_NAMES}")

    # [9] risk_level_id enum
    print("\n[9] risk_level_id enum 4个等级")
    level_enum = set(rec_fields.get("risk_level_id", {}).get("enum", []))
    if level_enum == VALID_RISK_LEVELS:
        ok("risk_level_id enum 4个等级全覆盖 ✓")
    else:
        fail(f"risk_level_id enum {level_enum} ≠ {VALID_RISK_LEVELS}")

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
    weight_sum = vr.get("indicator_weight_sum", 0)
    if weight_sum == 1.0:
        ok(f"validation_rules.indicator_weight_sum={weight_sum} = 1.0 ✓")
    else:
        fail(f"validation_rules.indicator_weight_sum={weight_sum} ≠ 1.0")
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
        print("  ✅ 教练脱落风险预警 schema 验证 PASS — 5指标/权重归一/⑤守护/七阶/六飞轮/MECE/PIPL 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
