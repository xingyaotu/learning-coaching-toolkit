#!/usr/bin/env python3
"""
道层教练学生档案 schema 验证脚本 v1.0
验证 pipeline-data/coaching-student-profile-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. student_profile_schema 7个必填字段
  3. current_stage/initial_stage/target_stage enum 七阶 + current_stage _dao_guard
  4. current_primary_bottleneck enum MECE + _dao_guard
  5. flywheel_mastery 六飞轮 + _dao_guard
  6. sop05_compliance_rate_lifetime ⑤守护
  7. stage_trajectory 七阶 enum + _dao_guard
  8. coaching_summary_stats: flywheels_mastered 六飞轮 + bottlenecks_resolved MECE
  9. validation_rules: sop05_guard/七阶/MECE/六飞轮/pipl
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PROFILE_PATH = REPO_ROOT / "pipeline-data" / "coaching-student-profile-schema.json"

VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}
MECE_DIMENSIONS = {"M", "E_exec", "C", "E_env"}
REQUIRED_PROFILE_FIELDS = {
    "profile_id", "student_id", "enrollment_date",
    "profile_status", "current_stage", "initial_stage", "total_sessions_completed"
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
    print("  教练学生档案 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not PROFILE_PATH.exists():
        fail(f"找不到文件: {PROFILE_PATH}")
        sys.exit(1)
    data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    ok("coaching-student-profile-schema.json 加载成功")

    fields = data.get("student_profile_schema", {}).get("fields", {})
    traj = data.get("stage_trajectory", {})
    summary = data.get("coaching_summary_stats", {}).get("fields", {})
    vr = data.get("validation_rules", {})

    # [2] student_profile_schema 7个必填字段
    print("\n[2] student_profile_schema 7个必填字段")
    vr_req = set(vr.get("required_profile_fields", []))
    if vr_req == REQUIRED_PROFILE_FIELDS:
        ok("validation_rules.required_profile_fields 7字段全覆盖 ✓")
    else:
        missing_rf = REQUIRED_PROFILE_FIELDS - vr_req
        fail(f"required_profile_fields 缺少: {missing_rf}")
    for fname in REQUIRED_PROFILE_FIELDS:
        if fname in fields:
            ok(f"student_profile_schema.fields.{fname} 存在 ✓")
        else:
            fail(f"student_profile_schema.fields.{fname} 缺失")

    # [3] stage enums 七阶 + current_stage _dao_guard
    print("\n[3] current_stage/initial_stage/target_stage enum 七阶 + _dao_guard")
    for fname in ["current_stage", "initial_stage", "target_stage"]:
        enum_val = set(fields.get(fname, {}).get("enum", []))
        if enum_val == VALID_STAGE_NAMES:
            ok(f"{fname} enum 七阶全覆盖 ✓")
        else:
            fail(f"{fname} enum {enum_val} ≠ {VALID_STAGE_NAMES}")
    cs_guard = fields.get("current_stage", {}).get("_dao_guard", "")
    if "七阶" in cs_guard:
        ok("current_stage._dao_guard 含'七阶' ✓")
    else:
        fail(f"current_stage._dao_guard='{cs_guard}' 未含'七阶'")

    # [4] current_primary_bottleneck enum MECE + _dao_guard
    print("\n[4] current_primary_bottleneck enum MECE + _dao_guard")
    bn_enum = set(fields.get("current_primary_bottleneck", {}).get("enum", []))
    if bn_enum == MECE_DIMENSIONS:
        ok("current_primary_bottleneck enum MECE 四维度 ✓")
    else:
        fail(f"current_primary_bottleneck enum {bn_enum} ≠ {MECE_DIMENSIONS}")
    bn_guard = fields.get("current_primary_bottleneck", {}).get("_dao_guard", "")
    if "MECE" in bn_guard:
        ok("current_primary_bottleneck._dao_guard 含'MECE' ✓")
    else:
        fail(f"current_primary_bottleneck._dao_guard='{bn_guard}' 未含'MECE'")

    # [5] flywheel_mastery 六飞轮 + _dao_guard
    print("\n[5] flywheel_mastery 六飞轮 + _dao_guard")
    fwm = fields.get("flywheel_mastery", {})
    fw_props = set(fwm.get("properties", {}).keys())
    if fw_props == VALID_FLYWHEEL_NAMES:
        ok("flywheel_mastery 六飞轮全覆盖 ✓")
    else:
        fail(f"flywheel_mastery properties {fw_props} ≠ {VALID_FLYWHEEL_NAMES}")
    fwm_guard = fwm.get("_dao_guard", "")
    if "六飞轮" in fwm_guard:
        ok("flywheel_mastery._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"flywheel_mastery._dao_guard='{fwm_guard}' 未含'六飞轮'")

    # [6] sop05_compliance_rate_lifetime ⑤守护
    print("\n[6] sop05_compliance_rate_lifetime ⑤守护")
    sop_field = fields.get("sop05_compliance_rate_lifetime", {})
    sop_guard = sop_field.get("_dao_guard", "")
    if "流程" in sop_guard:
        ok("sop05_compliance_rate_lifetime._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_compliance_rate_lifetime._dao_guard='{sop_guard}' 未含'流程'")

    # [7] stage_trajectory 七阶 enum + _dao_guard
    print("\n[7] stage_trajectory 七阶 enum + _dao_guard")
    te_schema = traj.get("trajectory_entry_schema", {})
    traj_stage_enum = set(te_schema.get("observed_stage", {}).get("enum", []))
    if traj_stage_enum == VALID_STAGE_NAMES:
        ok("stage_trajectory.observed_stage enum 七阶全覆盖 ✓")
    else:
        fail(f"trajectory observed_stage enum {traj_stage_enum} ≠ {VALID_STAGE_NAMES}")
    traj_guard = te_schema.get("observed_stage", {}).get("_dao_guard", "")
    if "七阶" in traj_guard:
        ok("stage_trajectory.observed_stage._dao_guard 含'七阶' ✓")
    else:
        fail(f"stage_trajectory observed_stage._dao_guard='{traj_guard}' 未含'七阶'")

    # [8] coaching_summary_stats
    print("\n[8] coaching_summary_stats flywheels_mastered + bottlenecks_resolved")
    fm_items = summary.get("flywheels_mastered", {}).get("items", {})
    fm_enum = set(fm_items.get("enum", []))
    if fm_enum == VALID_FLYWHEEL_NAMES:
        ok("flywheels_mastered.items enum 六飞轮全覆盖 ✓")
    else:
        fail(f"flywheels_mastered enum {fm_enum} ≠ {VALID_FLYWHEEL_NAMES}")
    fm_guard = summary.get("flywheels_mastered", {}).get("_dao_guard", "")
    if "六飞轮" in fm_guard:
        ok("flywheels_mastered._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"flywheels_mastered._dao_guard='{fm_guard}' 未含'六飞轮'")
    br_items = summary.get("bottlenecks_resolved", {}).get("items", {})
    br_enum = set(br_items.get("enum", []))
    if br_enum == MECE_DIMENSIONS:
        ok("bottlenecks_resolved.items enum MECE 四维度 ✓")
    else:
        fail(f"bottlenecks_resolved enum {br_enum} ≠ {MECE_DIMENSIONS}")

    # [9] validation_rules
    print("\n[9] validation_rules 合规")
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
        print("  ✅ 教练学生档案 schema 验证 PASS — 档案字段/⑤守护/七阶/MECE/六飞轮/PIPL 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
