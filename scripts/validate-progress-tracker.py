#!/usr/bin/env python3
"""
道层教练进度追踪 schema 验证脚本 v1.0
验证 pipeline-data/coaching-progress-tracker-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. 三种 record_schema 全覆盖 (session_progress_record / stage_progress_record / coaching_journey_summary)
  3. session_progress_record 核心字段完整性
  4. stage_progress_record 核心字段完整性
  5. coaching_journey_summary 核心字段完整性
  6. flywheels_practiced enum 值在六飞轮范围内
  7. ⑤守护: validation_rules step_id_5_name = '流程'
  8. validation_rules.six_flywheel_valid_names 枚举 6 个
  9. PIPL 合规声明存在
  10. tracker_templates 三模板全覆盖
  11. data_retention_rules 存在
  12. coach_performance_formula 系数之和 == 1.0
"""

import json
import sys
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TRACKER_PATH = REPO_ROOT / "pipeline-data" / "coaching-progress-tracker-schema.json"

REQUIRED_RECORD_SCHEMAS = {
    "session_progress_record",
    "stage_progress_record",
    "coaching_journey_summary",
}
REQUIRED_SESSION_FIELDS = {
    "record_id", "student_id", "session_id", "session_date", "goal_id",
    "subject", "current_stage", "session_template_id", "sop_ref",
    "kpi_results", "student_self_eval", "coach_eval", "completion_rate",
}
REQUIRED_STAGE_FIELDS = {
    "record_id", "student_id", "goal_id", "subject", "assessment_date",
    "previous_stage", "current_stage", "theta_before", "theta_after",
    "theta_delta", "stage_advanced", "mece_snapshot",
}
REQUIRED_SUMMARY_FIELDS = {
    "summary_id", "student_id", "goal_id", "subject",
    "total_sessions", "initial_stage", "current_stage",
    "stage_advances", "avg_student_eval", "avg_coach_eval",
    "avg_completion_rate", "flywheels_practiced", "goal_status",
    "coach_performance_score",
}
VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
REQUIRED_TEMPLATE_IDS = {"tpl-weekly-review", "tpl-milestone-check", "tpl-monthly-summary"}

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
    print("  教练进度追踪 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not TRACKER_PATH.exists():
        fail(f"找不到文件: {TRACKER_PATH}")
        sys.exit(1)
    data = json.loads(TRACKER_PATH.read_text(encoding="utf-8"))
    ok("coaching-progress-tracker-schema.json 加载成功")

    schemas = data.get("record_schemas", {})

    # [2] 三种 record_schema 全覆盖
    print("\n[2] record_schemas 三类全覆盖")
    found_schemas = set(schemas.keys())
    missing = REQUIRED_RECORD_SCHEMAS - found_schemas
    if missing:
        fail(f"缺少 record_schema: {missing}")
    else:
        ok(f"三类 record_schema 全覆盖 ✓")

    # [3] session_progress_record 字段
    print("\n[3] session_progress_record 核心字段")
    spr = schemas.get("session_progress_record", {}).get("fields", {})
    missing_spr = REQUIRED_SESSION_FIELDS - set(spr.keys())
    if missing_spr:
        fail(f"session_progress_record 缺少字段: {missing_spr}")
    else:
        ok(f"session_progress_record {len(spr)}个字段 核心字段全覆盖 ✓")

    # subject enum check
    subject_enum = spr.get("subject", {}).get("enum", [])
    if len(subject_enum) >= 9:
        ok(f"subject enum {len(subject_enum)}个科目 ✓")
    else:
        fail(f"subject enum 仅 {len(subject_enum)} 个科目 < 9")

    # stage range check
    stage_min = spr.get("current_stage", {}).get("minimum", 0)
    stage_max = spr.get("current_stage", {}).get("maximum", 0)
    if stage_min == 1 and stage_max == 7:
        ok("session current_stage range [1,7] ✓")
    else:
        fail(f"session current_stage range [{stage_min},{stage_max}] ≠ [1,7]")

    # eight_step_id range
    step_min = spr.get("eight_step_id", {}).get("minimum", 0)
    step_max = spr.get("eight_step_id", {}).get("maximum", 0)
    if step_min == 1 and step_max == 8:
        ok("session eight_step_id range [1,8] ✓")
    else:
        fail(f"session eight_step_id range [{step_min},{step_max}] ≠ [1,8]")

    # [4] stage_progress_record 字段
    print("\n[4] stage_progress_record 核心字段")
    stg = schemas.get("stage_progress_record", {}).get("fields", {})
    missing_stg = REQUIRED_STAGE_FIELDS - set(stg.keys())
    if missing_stg:
        fail(f"stage_progress_record 缺少字段: {missing_stg}")
    else:
        ok(f"stage_progress_record {len(stg)}个字段 核心字段全覆盖 ✓")

    # mece_snapshot properties
    mece_snap_props = stg.get("mece_snapshot", {}).get("properties", {})
    mece_keys = {"M_score", "E_exec_score", "C_theta", "E_env_score"}
    missing_mece = mece_keys - set(mece_snap_props.keys())
    if missing_mece:
        fail(f"mece_snapshot 缺少维度: {missing_mece}")
    else:
        ok(f"mece_snapshot 四维度 ✓ {sorted(mece_snap_props.keys())}")

    # [5] coaching_journey_summary 字段
    print("\n[5] coaching_journey_summary 核心字段")
    cjs = schemas.get("coaching_journey_summary", {}).get("fields", {})
    missing_cjs = REQUIRED_SUMMARY_FIELDS - set(cjs.keys())
    if missing_cjs:
        fail(f"coaching_journey_summary 缺少字段: {missing_cjs}")
    else:
        ok(f"coaching_journey_summary {len(cjs)}个字段 核心字段全覆盖 ✓")

    # [6] flywheels_practiced enum
    print("\n[6] flywheels_practiced 飞轮枚举验证")
    fw_items = cjs.get("flywheels_practiced", {}).get("items", {}).get("enum", [])
    if not fw_items:
        fail("flywheels_practiced items enum 缺失")
    else:
        fw_set = set(fw_items)
        invalid = fw_set - VALID_FLYWHEEL_NAMES
        if invalid:
            fail(f"flywheels_practiced 含非法飞轮: {invalid}")
        else:
            ok(f"flywheels_practiced enum {fw_items} 合规 ✓")

    # goal_status enum
    gs_enum = cjs.get("goal_status", {}).get("enum", [])
    if "on_track" in gs_enum and "completed" in gs_enum:
        ok(f"goal_status enum {gs_enum} 合规 ✓")
    else:
        fail(f"goal_status enum 缺少必要值: {gs_enum}")

    # [7] ⑤守护
    print("\n[7] ⑤守护验证")
    vr = data.get("validation_rules", {})
    step5_name = vr.get("eight_step_name_constraints", {}).get("step_id_5_name", "")
    if step5_name == "流程":
        ok("validation_rules step_id_5_name='流程' ⑤联动守护 ✓")
    else:
        fail(f"validation_rules step_id_5_name='{step5_name}' ≠ '流程'")

    # [8] six_flywheel_valid_names
    print("\n[8] six_flywheel_valid_names 枚举")
    fw_names = set(vr.get("six_flywheel_valid_names", []))
    missing_fw = VALID_FLYWHEEL_NAMES - fw_names
    if missing_fw:
        fail(f"six_flywheel_valid_names 缺少: {missing_fw}")
    elif len(fw_names) == 6:
        ok("six_flywheel_valid_names 六飞轮全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names 数量 {len(fw_names)} ≠ 6")

    # [9] PIPL 合规
    print("\n[9] PIPL 合规声明")
    pipl_meta = data.get("_meta", {}).get("pipl_note", "")
    pipl_vr = vr.get("pipl_constraints", "")
    if "PIPL" in pipl_meta and "匿名" in pipl_meta:
        ok("_meta.pipl_note PIPL 合规声明存在 ✓")
    else:
        fail("_meta.pipl_note 缺少 PIPL 合规声明")
    if "PIPL" in pipl_vr or "匿名" in pipl_vr:
        ok("validation_rules.pipl_constraints 存在 ✓")
    else:
        fail("validation_rules.pipl_constraints 缺失")

    # [10] tracker_templates
    print("\n[10] tracker_templates 三模板验证")
    templates = data.get("tracker_templates", [])
    found_tpl_ids = {t.get("template_id") for t in templates}
    missing_tpl = REQUIRED_TEMPLATE_IDS - found_tpl_ids
    if missing_tpl:
        fail(f"缺少 tracker_template: {missing_tpl}")
    else:
        ok(f"三模板全覆盖 ✓ {sorted(found_tpl_ids)}")
    for t in templates:
        tid = t.get("template_id", "?")
        if t.get("frequency") and t.get("required_records"):
            ok(f"{tid}: frequency + required_records 存在 ✓")
        else:
            fail(f"{tid}: 缺少 frequency 或 required_records")

    # [11] data_retention_rules
    print("\n[11] data_retention_rules 验证")
    drr = data.get("data_retention_rules", {})
    required_retention = {"session_progress_record", "stage_progress_record", "coaching_journey_summary"}
    found_ret = set(drr.keys())
    missing_ret = required_retention - found_ret
    if missing_ret:
        fail(f"data_retention_rules 缺少: {missing_ret}")
    else:
        ok("三类记录的数据保留规则全覆盖 ✓")
    if drr.get("pipl_delete_on_request") is True:
        ok("pipl_delete_on_request=true PIPL 合规 ✓")
    else:
        fail("pipl_delete_on_request 缺失或非 true")

    # [12] coach_performance_formula 系数之和
    print("\n[12] coach_performance_formula 系数之和")
    formula = vr.get("coach_performance_formula", "")
    coeffs = [float(x) for x in re.findall(r'(\d+\.\d+)\s*\*', formula)]
    if coeffs:
        total = sum(coeffs)
        if abs(total - 1.0) < 1e-9:
            ok(f"公式系数之和 = {total:.2f} ✓ ({coeffs})")
        else:
            fail(f"公式系数之和 = {total:.4f} ≠ 1.0")
    else:
        fail("coach_performance_formula 解析失败或系数缺失")

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
        print("  ✅ 教练进度追踪 schema 验证 PASS — 全部配置合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
