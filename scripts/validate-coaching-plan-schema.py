#!/usr/bin/env python3
"""
道层个性化教练计划 schema 验证脚本 v1.0
验证 pipeline-data/coaching-plan-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. coaching_plan_schema 核心字段: 8个必填
  3. diagnosis_basis: mece_profile 四维度 + _dao_guard + initial_stage 七阶枚举
  4. initial_flywheel_priorities 六飞轮枚举 + _dao_guard
  5. plan_goals items: target_stage 七阶枚举 + target_mece_dimension MECE
  6. sop_schedule: sop05_plan_note._dao_guard 含'流程' — ⑤守护
  7. flywheel_focus_schedule 三阶段飞轮 enum 六飞轮
  8. plan_template_defaults: 7个阶位默认配置 + 运用阶位 _dao_guard 含'sop-05'/'流程'
  9. validation_rules: 七阶/六飞轮/MECE/sop05_plan_guard/pipl
  10. PIPL 合规声明
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PLAN_PATH = REPO_ROOT / "pipeline-data" / "coaching-plan-schema.json"

VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}
MECE_DIMENSIONS = {"M", "E_exec", "C", "E_env"}
REQUIRED_PLAN_FIELDS = {
    "plan_id", "student_id", "coach_id", "plan_created_at",
    "diagnosis_basis", "plan_goals", "sop_schedule", "plan_status"
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
    print("  个性化教练计划 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not PLAN_PATH.exists():
        fail(f"找不到文件: {PLAN_PATH}")
        sys.exit(1)
    data = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    ok("coaching-plan-schema.json 加载成功")

    plan_fields = data.get("coaching_plan_schema", {}).get("fields", {})
    vr = data.get("validation_rules", {})

    # [2] 核心字段
    print("\n[2] coaching_plan_schema 8个核心字段")
    vr_fields = set(vr.get("required_fields", []))
    if vr_fields == REQUIRED_PLAN_FIELDS:
        ok(f"validation_rules.required_fields 8字段全覆盖 ✓")
    else:
        missing_rf = REQUIRED_PLAN_FIELDS - vr_fields
        fail(f"required_fields 缺少: {missing_rf}")
    for fname in REQUIRED_PLAN_FIELDS:
        if fname in plan_fields:
            ok(f"coaching_plan_schema.fields.{fname} 存在 ✓")
        else:
            fail(f"coaching_plan_schema.fields.{fname} 缺失")

    # [3] diagnosis_basis mece_profile + initial_stage
    print("\n[3] diagnosis_basis MECE 四维度 + 七阶 initial_stage")
    db = plan_fields.get("diagnosis_basis", {})
    mece_props = db.get("properties", {}).get("mece_profile", {}).get("properties", {})
    mece_theta_keys = {k.replace("_theta", "") for k in mece_props.keys() if k.endswith("_theta")}
    if mece_theta_keys == MECE_DIMENSIONS:
        ok(f"diagnosis_basis.mece_profile 四维度 {sorted(mece_theta_keys)} ✓")
    else:
        fail(f"diagnosis_basis.mece_profile 维度 {mece_theta_keys} ≠ {MECE_DIMENSIONS}")
    bottleneck_enum = set(mece_props.get("primary_bottleneck", {}).get("enum", []))
    if bottleneck_enum == MECE_DIMENSIONS:
        ok("mece_profile.primary_bottleneck enum MECE 四维度 ✓")
    else:
        fail(f"primary_bottleneck enum {bottleneck_enum} ≠ {MECE_DIMENSIONS}")
    mece_guard = str(db.get("properties", {}).get("mece_profile", {}).get("_dao_guard", ""))
    if "MECE" in mece_guard:
        ok("mece_profile._dao_guard 含'MECE' ✓")
    else:
        fail(f"mece_profile._dao_guard='{mece_guard}' 未含'MECE'")

    initial_stage_enum = set(db.get("properties", {}).get("initial_stage", {}).get("enum", []))
    if initial_stage_enum == VALID_STAGE_NAMES:
        ok("diagnosis_basis.initial_stage enum 七阶全覆盖 ✓")
    else:
        fail(f"initial_stage enum {initial_stage_enum} ≠ {VALID_STAGE_NAMES}")

    # [4] initial_flywheel_priorities 六飞轮 + _dao_guard
    print("\n[4] initial_flywheel_priorities 六飞轮枚举 + _dao_guard")
    fw_prio = db.get("properties", {}).get("initial_flywheel_priorities", {})
    fw_enum = set(fw_prio.get("items", {}).get("enum", []))
    if fw_enum == VALID_FLYWHEEL_NAMES:
        ok("initial_flywheel_priorities enum 六飞轮全覆盖 ✓")
    else:
        fail(f"initial_flywheel_priorities enum {fw_enum} ≠ {VALID_FLYWHEEL_NAMES}")
    fw_guard = fw_prio.get("_dao_guard", "")
    if "六飞轮" in fw_guard:
        ok("initial_flywheel_priorities._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"initial_flywheel_priorities._dao_guard='{fw_guard}' 未含'六飞轮'")

    # [5] plan_goals items
    print("\n[5] plan_goals items 七阶/MECE 枚举")
    pg_items = plan_fields.get("plan_goals", {}).get("items", {})
    ts_enum = set(pg_items.get("target_stage", {}).get("enum", []))
    if ts_enum == VALID_STAGE_NAMES:
        ok("plan_goals.target_stage enum 七阶全覆盖 ✓")
    else:
        fail(f"plan_goals.target_stage enum {ts_enum} ≠ {VALID_STAGE_NAMES}")
    tmd_enum = set(pg_items.get("target_mece_dimension", {}).get("enum", []))
    if MECE_DIMENSIONS <= tmd_enum:
        ok(f"plan_goals.target_mece_dimension enum 含 MECE 四维度 ✓")
    else:
        fail(f"plan_goals.target_mece_dimension enum {tmd_enum} 未含全部 MECE")
    status_enum = set(pg_items.get("status", {}).get("enum", []))
    if status_enum:
        ok(f"plan_goals.status enum {len(status_enum)}个选项 ✓")
    else:
        fail("plan_goals.status enum 为空")

    # [6] sop_schedule sop05_plan_note ⑤守护
    print("\n[6] sop_schedule ⑤守护 — sop05_plan_note 含'流程'")
    ss = plan_fields.get("sop_schedule", {}).get("properties", {})
    sop05_note = ss.get("sop05_plan_note", {})
    sop05_guard = sop05_note.get("_dao_guard", "")
    if "流程" in sop05_guard:
        ok("sop05_plan_note._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_plan_note._dao_guard='{sop05_guard}' 未含'流程'")
    if "sop05_plan_note" in ss:
        ok("sop_schedule.sop05_plan_note 字段存在 ✓")
    else:
        fail("sop_schedule.sop05_plan_note 字段缺失")

    # [7] flywheel_focus_schedule 三阶段飞轮枚举
    print("\n[7] flywheel_focus_schedule 三阶段六飞轮枚举")
    ffs = plan_fields.get("flywheel_focus_schedule", {}).get("properties", {})
    for phase in ["phase1_flywheels", "phase2_flywheels", "phase3_flywheels"]:
        phase_enum = set(ffs.get(phase, {}).get("items", {}).get("enum", []))
        if phase_enum == VALID_FLYWHEEL_NAMES:
            ok(f"flywheel_focus_schedule.{phase} enum 六飞轮全覆盖 ✓")
        else:
            fail(f"flywheel_focus_schedule.{phase} enum {phase_enum} ≠ {VALID_FLYWHEEL_NAMES}")

    # [8] plan_template_defaults 7个阶位 + 运用阶位
    print("\n[8] plan_template_defaults 七阶默认配置")
    ptd = data.get("plan_template_defaults", {})
    stage_defaults = ptd.get("stage_defaults", [])
    if len(stage_defaults) == 7:
        ok(f"plan_template_defaults.stage_defaults 7个阶位 ✓")
    else:
        fail(f"plan_template_defaults.stage_defaults {len(stage_defaults)} ≠ 7")

    stage_names_in_defaults = {s.get("stage") for s in stage_defaults}
    if stage_names_in_defaults == VALID_STAGE_NAMES:
        ok("stage_defaults 七阶全覆盖 ✓")
    else:
        fail(f"stage_defaults 阶位 {stage_names_in_defaults} ≠ {VALID_STAGE_NAMES}")

    yunyong = next((s for s in stage_defaults if s.get("stage") == "运用"), None)
    if yunyong:
        guard_yy = yunyong.get("_dao_guard", "")
        if "sop-05" in guard_yy and "流程" in guard_yy:
            ok("运用阶位 _dao_guard 含 sop-05 和'流程' ⑤守护 ✓")
        else:
            fail(f"运用阶位 _dao_guard='{guard_yy}' 未含 sop-05 和'流程'")
    else:
        fail("plan_template_defaults 未含运用阶位")

    # [9] validation_rules
    print("\n[9] validation_rules 合规")
    sd_count = vr.get("stage_defaults_count", 0)
    if sd_count == 7:
        ok("validation_rules.stage_defaults_count=7 ✓")
    else:
        fail(f"validation_rules.stage_defaults_count={sd_count} ≠ 7")

    fw_names = set(vr.get("six_flywheel_valid_names", []))
    if fw_names == VALID_FLYWHEEL_NAMES:
        ok("validation_rules.six_flywheel_valid_names 六飞轮全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names {fw_names} ≠ {VALID_FLYWHEEL_NAMES}")

    stage_names_vr = set(vr.get("seven_stage_valid_names", []))
    if stage_names_vr == VALID_STAGE_NAMES:
        ok("validation_rules.seven_stage_valid_names 七阶全覆盖 ✓")
    else:
        fail(f"seven_stage_valid_names {stage_names_vr} ≠ {VALID_STAGE_NAMES}")

    mece_codes = set(vr.get("mece_dimension_codes", []))
    if mece_codes == MECE_DIMENSIONS:
        ok("validation_rules.mece_dimension_codes MECE 四维度 ✓")
    else:
        fail(f"mece_dimension_codes {mece_codes} ≠ {MECE_DIMENSIONS}")

    sop05_guard_vr = vr.get("sop05_plan_guard", "")
    if "流程" in sop05_guard_vr:
        ok("validation_rules.sop05_plan_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"validation_rules.sop05_plan_guard='{sop05_guard_vr}' 未含'流程'")

    # [10] PIPL 合规
    print("\n[10] PIPL 合规")
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
        print("  ✅ 个性化教练计划 schema 验证 PASS — MECE/七阶/六飞轮/⑤守护 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
