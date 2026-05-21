#!/usr/bin/env python3
"""
道层教练平台分析 schema 验证脚本 v1.0
验证 pipeline-data/coaching-platform-analytics-schema.json 的合规性。
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
ANALYTICS_PATH = REPO_ROOT / "pipeline-data" / "coaching-platform-analytics-schema.json"

VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}
MECE_DIMENSIONS = {"M", "E_exec", "C", "E_env"}

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
    print("  教练平台分析 schema 验证 v1.0")
    print("=" * 62)

    print("\n[1] 文件加载")
    if not ANALYTICS_PATH.exists():
        fail(f"找不到文件: {ANALYTICS_PATH}")
        sys.exit(1)
    data = json.loads(ANALYTICS_PATH.read_text(encoding="utf-8"))
    ok("coaching-platform-analytics-schema.json 加载成功")

    pa_fields = data.get("platform_analytics_schema", {}).get("fields", {})
    coach_perf = data.get("coach_performance_summary", {}).get("fields", {})
    trend = data.get("trend_analysis", {})
    mcsr = data.get("minimum_cell_size_rule", {})
    vr = data.get("validation_rules", {})

    print("\n[2] stage_distribution_platform 七阶全覆盖 + _dao_guard")
    sd = pa_fields.get("stage_distribution_platform", {})
    sd_props = set(sd.get("properties", {}).keys())
    if sd_props == VALID_STAGE_NAMES:
        ok("stage_distribution_platform 七阶全覆盖 ✓")
    else:
        fail(f"stage_distribution_platform props {sd_props} ≠ {VALID_STAGE_NAMES}")
    sd_guard = sd.get("_dao_guard", "")
    if "七阶" in sd_guard and "1.0" in sd_guard:
        ok("stage_distribution_platform._dao_guard 含'七阶'+'1.0' ✓")
    else:
        fail(f"stage_distribution_platform._dao_guard='{sd_guard}' 未含'七阶'或'1.0'")

    print("\n[3] stage_advance_rate _dao_guard 含'七阶'")
    sar_guard = pa_fields.get("stage_advance_rate", {}).get("_dao_guard", "")
    if "七阶" in sar_guard:
        ok("stage_advance_rate._dao_guard 含'七阶' ✓")
    else:
        fail(f"stage_advance_rate._dao_guard='{sar_guard}' 未含'七阶'")

    print("\n[4] bottleneck_distribution_platform MECE 四维度 + _dao_guard")
    bd = pa_fields.get("bottleneck_distribution_platform", {})
    bd_props = set(bd.get("properties", {}).keys())
    if bd_props == MECE_DIMENSIONS:
        ok("bottleneck_distribution_platform MECE 四维度 ✓")
    else:
        fail(f"bottleneck_distribution_platform {bd_props} ≠ {MECE_DIMENSIONS}")
    bd_guard = bd.get("_dao_guard", "")
    if "MECE" in bd_guard and "1.0" in bd_guard:
        ok("bottleneck_distribution_platform._dao_guard 含'MECE'+'1.0' ✓")
    else:
        fail(f"bottleneck_distribution_platform._dao_guard='{bd_guard}' 未含'MECE'或'1.0'")

    print("\n[5] flywheel_mastery_platform_means 六飞轮 + _dao_guard")
    fwm = pa_fields.get("flywheel_mastery_platform_means", {})
    fw_props = set(fwm.get("properties", {}).keys())
    if fw_props == VALID_FLYWHEEL_NAMES:
        ok("flywheel_mastery_platform_means 六飞轮全覆盖 ✓")
    else:
        fail(f"flywheel_mastery_platform_means {fw_props} ≠ {VALID_FLYWHEEL_NAMES}")
    fwm_guard = fwm.get("_dao_guard", "")
    if "六飞轮" in fwm_guard:
        ok("flywheel_mastery_platform_means._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"flywheel_mastery_platform_means._dao_guard='{fwm_guard}' 未含'六飞轮'")

    print("\n[6] sop05_compliance_rate_platform ⑤守护 含'流程'")
    sop_guard = pa_fields.get("sop05_compliance_rate_platform", {}).get("_dao_guard", "")
    if "流程" in sop_guard:
        ok("sop05_compliance_rate_platform._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_compliance_rate_platform._dao_guard='{sop_guard}' 未含'流程'")

    print("\n[7] most_common_stage_platform enum 七阶 + _dao_guard")
    mcs_field = pa_fields.get("most_common_stage_platform", {})
    mcs_enum = set(mcs_field.get("enum", []))
    if mcs_enum == VALID_STAGE_NAMES:
        ok("most_common_stage_platform enum 七阶全覆盖 ✓")
    else:
        fail(f"most_common_stage_platform enum {mcs_enum} ≠ {VALID_STAGE_NAMES}")
    mcs_guard = mcs_field.get("_dao_guard", "")
    if "七阶" in mcs_guard:
        ok("most_common_stage_platform._dao_guard 含'七阶' ✓")
    else:
        fail(f"most_common_stage_platform._dao_guard='{mcs_guard}' 未含'七阶'")

    print("\n[8] weakest_flywheel_platform enum 六飞轮 + _dao_guard")
    wfp_field = pa_fields.get("weakest_flywheel_platform", {})
    wfp_enum = set(wfp_field.get("enum", []))
    if wfp_enum == VALID_FLYWHEEL_NAMES:
        ok("weakest_flywheel_platform enum 六飞轮全覆盖 ✓")
    else:
        fail(f"weakest_flywheel_platform enum {wfp_enum} ≠ {VALID_FLYWHEEL_NAMES}")
    wfp_guard = wfp_field.get("_dao_guard", "")
    if "六飞轮" in wfp_guard:
        ok("weakest_flywheel_platform._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"weakest_flywheel_platform._dao_guard='{wfp_guard}' 未含'六飞轮'")

    print("\n[9] trend_analysis 七阶/六飞轮/sop05 enum_guard + _dao_guard")
    stage_trend = trend.get("stage_distribution_trend", {})
    stage_eg = set(stage_trend.get("stage_enum_guard", []))
    if stage_eg == VALID_STAGE_NAMES:
        ok("trend_analysis.stage_distribution_trend.stage_enum_guard 七阶全覆盖 ✓")
    else:
        fail(f"stage_trend.stage_enum_guard {stage_eg} ≠ {VALID_STAGE_NAMES}")
    st_guard = stage_trend.get("_dao_guard", "")
    if "七阶" in st_guard:
        ok("stage_distribution_trend._dao_guard 含'七阶' ✓")
    else:
        fail(f"stage_distribution_trend._dao_guard='{st_guard}' 未含'七阶'")
    fw_trend = trend.get("flywheel_trend", {})
    fw_eg = set(fw_trend.get("flywheel_enum_guard", []))
    if fw_eg == VALID_FLYWHEEL_NAMES:
        ok("trend_analysis.flywheel_trend.flywheel_enum_guard 六飞轮全覆盖 ✓")
    else:
        fail(f"flywheel_trend.flywheel_enum_guard {fw_eg} ≠ {VALID_FLYWHEEL_NAMES}")
    fw_t_guard = fw_trend.get("_dao_guard", "")
    if "六飞轮" in fw_t_guard:
        ok("flywheel_trend._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"flywheel_trend._dao_guard='{fw_t_guard}' 未含'六飞轮'")
    sop05_trend = trend.get("sop05_compliance_trend", {})
    sop05_t_guard = sop05_trend.get("_dao_guard", "")
    if "流程" in sop05_t_guard:
        ok("sop05_compliance_trend._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_compliance_trend._dao_guard='{sop05_t_guard}' 未含'流程'")

    print("\n[10] minimum_cell_size_rule min=50 + _dao_guard 含'PIPL'")
    min_cell = mcsr.get("min_cell_size", 0)
    if min_cell >= 50:
        ok(f"minimum_cell_size_rule.min_cell_size={min_cell} ≥ 50 ✓")
    else:
        fail(f"minimum_cell_size_rule.min_cell_size={min_cell} < 50")
    mcsr_guard = mcsr.get("_dao_guard", "")
    if "PIPL" in mcsr_guard:
        ok("minimum_cell_size_rule._dao_guard 含'PIPL' ✓")
    else:
        fail(f"minimum_cell_size_rule._dao_guard='{mcsr_guard}' 未含'PIPL'")

    print("\n[11] coach_performance_summary avg_sop05_compliance_rate ⑤守护")
    cps_sop_guard = coach_perf.get("avg_sop05_compliance_rate", {}).get("_dao_guard", "")
    if "流程" in cps_sop_guard:
        ok("coach_performance_summary.avg_sop05_compliance_rate._dao_guard 含'流程' ✓")
    else:
        fail(f"avg_sop05_compliance_rate._dao_guard='{cps_sop_guard}' 未含'流程'")

    print("\n[12] validation_rules 合规")
    sop05_guard_vr = vr.get("sop05_guard", "")
    if "流程" in sop05_guard_vr:
        ok("validation_rules.sop05_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"validation_rules.sop05_guard='{sop05_guard_vr}' 未含'流程'")
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
        print("  ✅ 教练平台分析 schema 验证 PASS — 七阶/MECE/六飞轮/⑤守护/趋势/最小样本/PIPL 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
