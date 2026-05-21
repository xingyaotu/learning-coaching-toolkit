#!/usr/bin/env python3
"""
道层教练职业发展 schema 验证脚本 v1.0
验证 pipeline-data/coaching-coach-development-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. coach_development_record_schema: 4个必填字段
  3. current_certification_level enum ccl-1至ccl-5 + _dao_guard
  4. sop05_training_completed _dao_guard 含'流程' ⑤守护
  5. sop05_training_date _dao_guard 含'流程' ⑤守护
  6. cpd_hours_by_domain _dao_guard 含'飞轮'+'七阶'+'MECE'
  7. flywheel_teaching_competency: competency_by_flywheel 六飞轮 + _dao_guard
  8. weakest_flywheel_teaching enum 六飞轮 + _dao_guard
  9. stage_teaching_competency: competency_by_stage 七阶 + _dao_guard
  10. max_eligible_stage_to_coach enum 七阶 + _dao_guard
  11. certification_progression: sop05_mastery_required ⑤守护
  12. validation_rules: sop05_guard/七阶/MECE/六飞轮/pipl
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DEV_PATH = REPO_ROOT / "pipeline-data" / "coaching-coach-development-schema.json"

VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}
MECE_DIMENSIONS = {"M", "E_exec", "C", "E_env"}
CERTIFICATION_LEVELS = {"ccl-1", "ccl-2", "ccl-3", "ccl-4", "ccl-5"}
REQUIRED_DEV_FIELDS = {
    "cpd_record_id", "coach_id", "current_certification_level", "sop05_training_completed"
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
    print("  教练职业发展 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not DEV_PATH.exists():
        fail(f"找不到文件: {DEV_PATH}")
        sys.exit(1)
    data = json.loads(DEV_PATH.read_text(encoding="utf-8"))
    ok("coaching-coach-development-schema.json 加载成功")

    cd_fields = data.get("coach_development_record_schema", {}).get("fields", {})
    ftc_fields = data.get("flywheel_teaching_competency", {}).get("fields", {})
    stc_fields = data.get("stage_teaching_competency", {}).get("fields", {})
    cp_fields = data.get("certification_progression", {}).get("fields", {})
    vr = data.get("validation_rules", {})

    # [2] 4个必填字段
    print("\n[2] coach_development_record_schema 4个必填字段")
    for fname in REQUIRED_DEV_FIELDS:
        if fname in cd_fields:
            ok(f"coach_development_record_schema.fields.{fname} 存在 ✓")
        else:
            fail(f"coach_development_record_schema.fields.{fname} 缺失")

    # [3] current_certification_level enum ccl-1至ccl-5 + _dao_guard
    print("\n[3] current_certification_level enum ccl-1至ccl-5 + _dao_guard")
    ccl_field = cd_fields.get("current_certification_level", {})
    ccl_enum = set(ccl_field.get("enum", []))
    if ccl_enum == CERTIFICATION_LEVELS:
        ok("current_certification_level enum ccl-1至ccl-5 ✓")
    else:
        fail(f"current_certification_level enum {ccl_enum} ≠ {CERTIFICATION_LEVELS}")
    ccl_guard = ccl_field.get("_dao_guard", "")
    if "ccl" in ccl_guard:
        ok("current_certification_level._dao_guard 含认证等级 ✓")
    else:
        fail(f"current_certification_level._dao_guard='{ccl_guard}' 未含'ccl'")

    # [4] sop05_training_completed ⑤守护
    print("\n[4] sop05_training_completed ⑤守护 含'流程'")
    stc_guard = cd_fields.get("sop05_training_completed", {}).get("_dao_guard", "")
    if "流程" in stc_guard:
        ok("sop05_training_completed._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_training_completed._dao_guard='{stc_guard}' 未含'流程'")

    # [5] sop05_training_date ⑤守护
    print("\n[5] sop05_training_date ⑤守护 含'流程'")
    std_guard = cd_fields.get("sop05_training_date", {}).get("_dao_guard", "")
    if "流程" in std_guard:
        ok("sop05_training_date._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_training_date._dao_guard='{std_guard}' 未含'流程'")

    # [6] cpd_hours_by_domain _dao_guard 含'飞轮'+'七阶'+'MECE'
    print("\n[6] cpd_hours_by_domain _dao_guard 含'飞轮'+'七阶'+'MECE'")
    chbd_guard = cd_fields.get("cpd_hours_by_domain", {}).get("_dao_guard", "")
    if "飞轮" in chbd_guard and "七阶" in chbd_guard and "MECE" in chbd_guard:
        ok("cpd_hours_by_domain._dao_guard 含'飞轮'+'七阶'+'MECE' ✓")
    else:
        fail(f"cpd_hours_by_domain._dao_guard='{chbd_guard}' 缺少关键词")

    # [7] flywheel_teaching_competency: competency_by_flywheel 六飞轮 + _dao_guard
    print("\n[7] flywheel_teaching_competency competency_by_flywheel 六飞轮 + _dao_guard")
    cbf_field = ftc_fields.get("competency_by_flywheel", {})
    cbf_props = set(cbf_field.get("properties", {}).keys())
    if cbf_props == VALID_FLYWHEEL_NAMES:
        ok("competency_by_flywheel 六飞轮全覆盖 ✓")
    else:
        fail(f"competency_by_flywheel {cbf_props} ≠ {VALID_FLYWHEEL_NAMES}")
    cbf_guard = cbf_field.get("_dao_guard", "")
    if "六飞轮" in cbf_guard:
        ok("competency_by_flywheel._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"competency_by_flywheel._dao_guard='{cbf_guard}' 未含'六飞轮'")

    # [8] weakest_flywheel_teaching enum 六飞轮 + _dao_guard
    print("\n[8] flywheel_teaching_competency weakest_flywheel_teaching enum 六飞轮 + _dao_guard")
    wft_field = ftc_fields.get("weakest_flywheel_teaching", {})
    wft_enum = set(wft_field.get("enum", []))
    if wft_enum == VALID_FLYWHEEL_NAMES:
        ok("weakest_flywheel_teaching enum 六飞轮全覆盖 ✓")
    else:
        fail(f"weakest_flywheel_teaching enum {wft_enum} ≠ {VALID_FLYWHEEL_NAMES}")
    wft_guard = wft_field.get("_dao_guard", "")
    if "六飞轮" in wft_guard:
        ok("weakest_flywheel_teaching._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"weakest_flywheel_teaching._dao_guard='{wft_guard}' 未含'六飞轮'")

    # [9] stage_teaching_competency: competency_by_stage 七阶 + _dao_guard
    print("\n[9] stage_teaching_competency competency_by_stage 七阶 + _dao_guard")
    cbs_field = stc_fields.get("competency_by_stage", {})
    cbs_props = set(cbs_field.get("properties", {}).keys())
    if cbs_props == VALID_STAGE_NAMES:
        ok("competency_by_stage 七阶全覆盖 ✓")
    else:
        fail(f"competency_by_stage {cbs_props} ≠ {VALID_STAGE_NAMES}")
    cbs_guard = cbs_field.get("_dao_guard", "")
    if "七阶" in cbs_guard:
        ok("competency_by_stage._dao_guard 含'七阶' ✓")
    else:
        fail(f"competency_by_stage._dao_guard='{cbs_guard}' 未含'七阶'")

    # [10] max_eligible_stage_to_coach enum 七阶 + _dao_guard
    print("\n[10] stage_teaching_competency max_eligible_stage_to_coach enum 七阶 + _dao_guard")
    mesc_field = stc_fields.get("max_eligible_stage_to_coach", {})
    mesc_enum = set(mesc_field.get("enum", []))
    if mesc_enum == VALID_STAGE_NAMES:
        ok("max_eligible_stage_to_coach enum 七阶全覆盖 ✓")
    else:
        fail(f"max_eligible_stage_to_coach enum {mesc_enum} ≠ {VALID_STAGE_NAMES}")
    mesc_guard = mesc_field.get("_dao_guard", "")
    if "七阶" in mesc_guard:
        ok("max_eligible_stage_to_coach._dao_guard 含'七阶' ✓")
    else:
        fail(f"max_eligible_stage_to_coach._dao_guard='{mesc_guard}' 未含'七阶'")

    # [11] certification_progression: sop05_mastery_required ⑤守护
    print("\n[11] certification_progression sop05_mastery_required ⑤守护 含'流程'")
    smr_guard = cp_fields.get("sop05_mastery_required", {}).get("_dao_guard", "")
    if "流程" in smr_guard:
        ok("sop05_mastery_required._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_mastery_required._dao_guard='{smr_guard}' 未含'流程'")

    # [12] validation_rules
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
    ccl_vr = set(vr.get("certification_levels", []))
    if ccl_vr == CERTIFICATION_LEVELS:
        ok("validation_rules.certification_levels ccl-1至ccl-5 ✓")
    else:
        fail(f"certification_levels {ccl_vr} ≠ {CERTIFICATION_LEVELS}")
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
        print("  ✅ 教练职业发展 schema 验证 PASS — CPD/认证/⑤守护/七阶/六飞轮/PIPL 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
