#!/usr/bin/env python3
"""
道层教练目标复核 schema 验证脚本 v1.0
验证 pipeline-data/coaching-goal-review-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. goal_review_schema: 6个必填字段
  3. review_trigger enum + _dao_guard 含'七阶'+'MECE'
  4. stage_at_review enum 七阶 + _dao_guard
  5. original_target_stage enum 七阶 + _dao_guard
  6. current_primary_bottleneck enum MECE + _dao_guard
  7. sop05_compliance_trend_at_review ⑤守护 含'流程'
  8. goal_review_decision enum + _dao_guard
  9. new_target_stage enum 七阶 + _dao_guard
  10. flywheel_priority_update enum 六飞轮 + _dao_guard
  11. review_progress_summary: stage_advances _dao_guard 含'七阶'
  12. flywheel_progress_since_last_review 六飞轮 + _dao_guard
  13. sop05_compliance_rate_since_last_review ⑤守护
  14. validation_rules: sop05_guard/七阶/MECE/六飞轮/pipl
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
REVIEW_PATH = REPO_ROOT / "pipeline-data" / "coaching-goal-review-schema.json"

VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}
MECE_DIMENSIONS = {"M", "E_exec", "C", "E_env"}
REQUIRED_REVIEW_FIELDS = {
    "review_id", "coaching_plan_id", "student_id",
    "coach_id", "review_date", "review_trigger"
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
    print("  教练目标复核 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not REVIEW_PATH.exists():
        fail(f"找不到文件: {REVIEW_PATH}")
        sys.exit(1)
    data = json.loads(REVIEW_PATH.read_text(encoding="utf-8"))
    ok("coaching-goal-review-schema.json 加载成功")

    gr_fields = data.get("goal_review_schema", {}).get("fields", {})
    rps_fields = data.get("review_progress_summary", {}).get("fields", {})
    vr = data.get("validation_rules", {})

    # [2] 6个必填字段
    print("\n[2] goal_review_schema 6个必填字段")
    for fname in REQUIRED_REVIEW_FIELDS:
        if fname in gr_fields:
            ok(f"goal_review_schema.fields.{fname} 存在 ✓")
        else:
            fail(f"goal_review_schema.fields.{fname} 缺失")

    # [3] review_trigger enum + _dao_guard 含'七阶'+'MECE'
    print("\n[3] review_trigger enum + _dao_guard 含'七阶'+'MECE'")
    rt_field = gr_fields.get("review_trigger", {})
    rt_enum = set(rt_field.get("enum", []))
    expected_rt = {"rt-scheduled", "rt-stage-advance", "rt-stage-regression",
                   "rt-bottleneck-shift", "rt-milestone-reached", "rt-dropout-risk"}
    if rt_enum == expected_rt:
        ok("review_trigger enum 六种触发 ✓")
    else:
        fail(f"review_trigger enum {rt_enum} ≠ {expected_rt}")
    rt_guard = rt_field.get("_dao_guard", "")
    if "七阶" in rt_guard and "MECE" in rt_guard:
        ok("review_trigger._dao_guard 含'七阶'+'MECE' ✓")
    else:
        fail(f"review_trigger._dao_guard='{rt_guard}' 未含全部关键词")

    # [4] stage_at_review enum 七阶 + _dao_guard
    print("\n[4] stage_at_review enum 七阶 + _dao_guard")
    sar_field = gr_fields.get("stage_at_review", {})
    sar_enum = set(sar_field.get("enum", []))
    if sar_enum == VALID_STAGE_NAMES:
        ok("stage_at_review enum 七阶全覆盖 ✓")
    else:
        fail(f"stage_at_review enum {sar_enum} ≠ {VALID_STAGE_NAMES}")
    sar_guard = sar_field.get("_dao_guard", "")
    if "七阶" in sar_guard:
        ok("stage_at_review._dao_guard 含'七阶' ✓")
    else:
        fail(f"stage_at_review._dao_guard='{sar_guard}' 未含'七阶'")

    # [5] original_target_stage enum 七阶 + _dao_guard
    print("\n[5] original_target_stage enum 七阶 + _dao_guard")
    ots_field = gr_fields.get("original_target_stage", {})
    ots_enum = set(ots_field.get("enum", []))
    if ots_enum == VALID_STAGE_NAMES:
        ok("original_target_stage enum 七阶全覆盖 ✓")
    else:
        fail(f"original_target_stage enum {ots_enum} ≠ {VALID_STAGE_NAMES}")
    ots_guard = ots_field.get("_dao_guard", "")
    if "七阶" in ots_guard:
        ok("original_target_stage._dao_guard 含'七阶' ✓")
    else:
        fail(f"original_target_stage._dao_guard='{ots_guard}' 未含'七阶'")

    # [6] current_primary_bottleneck enum MECE + _dao_guard
    print("\n[6] current_primary_bottleneck enum MECE + _dao_guard")
    cpb_field = gr_fields.get("current_primary_bottleneck", {})
    cpb_enum = set(cpb_field.get("enum", []))
    if cpb_enum == MECE_DIMENSIONS:
        ok("current_primary_bottleneck enum MECE 四维度 ✓")
    else:
        fail(f"current_primary_bottleneck enum {cpb_enum} ≠ {MECE_DIMENSIONS}")
    cpb_guard = cpb_field.get("_dao_guard", "")
    if "MECE" in cpb_guard:
        ok("current_primary_bottleneck._dao_guard 含'MECE' ✓")
    else:
        fail(f"current_primary_bottleneck._dao_guard='{cpb_guard}' 未含'MECE'")

    # [7] sop05_compliance_trend_at_review ⑤守护
    print("\n[7] sop05_compliance_trend_at_review ⑤守护 含'流程'")
    sctr_guard = gr_fields.get("sop05_compliance_trend_at_review", {}).get("_dao_guard", "")
    if "流程" in sctr_guard:
        ok("sop05_compliance_trend_at_review._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_compliance_trend_at_review._dao_guard='{sctr_guard}' 未含'流程'")

    # [8] goal_review_decision enum + _dao_guard
    print("\n[8] goal_review_decision enum + _dao_guard")
    grd_field = gr_fields.get("goal_review_decision", {})
    grd_enum = set(grd_field.get("enum", []))
    expected_grd = {"gr-continue", "gr-adjust-target", "gr-adjust-plan", "gr-escalate", "gr-graduate"}
    if grd_enum == expected_grd:
        ok("goal_review_decision enum 五种决策 ✓")
    else:
        fail(f"goal_review_decision enum {grd_enum} ≠ {expected_grd}")
    grd_guard = grd_field.get("_dao_guard", "")
    if "gr-continue" in grd_guard:
        ok("goal_review_decision._dao_guard 含决策枚举 ✓")
    else:
        fail(f"goal_review_decision._dao_guard='{grd_guard}' 未含枚举值")

    # [9] new_target_stage enum 七阶 + _dao_guard
    print("\n[9] new_target_stage enum 七阶 + _dao_guard")
    nts_field = gr_fields.get("new_target_stage", {})
    nts_enum = set(nts_field.get("enum", []))
    if nts_enum == VALID_STAGE_NAMES:
        ok("new_target_stage enum 七阶全覆盖 ✓")
    else:
        fail(f"new_target_stage enum {nts_enum} ≠ {VALID_STAGE_NAMES}")
    nts_guard = nts_field.get("_dao_guard", "")
    if "七阶" in nts_guard:
        ok("new_target_stage._dao_guard 含'七阶' ✓")
    else:
        fail(f"new_target_stage._dao_guard='{nts_guard}' 未含'七阶'")

    # [10] flywheel_priority_update enum 六飞轮 + _dao_guard
    print("\n[10] flywheel_priority_update enum 六飞轮 + _dao_guard")
    fpu_field = gr_fields.get("flywheel_priority_update", {})
    fpu_enum = set(fpu_field.get("enum", []))
    if fpu_enum == VALID_FLYWHEEL_NAMES:
        ok("flywheel_priority_update enum 六飞轮全覆盖 ✓")
    else:
        fail(f"flywheel_priority_update enum {fpu_enum} ≠ {VALID_FLYWHEEL_NAMES}")
    fpu_guard = fpu_field.get("_dao_guard", "")
    if "六飞轮" in fpu_guard:
        ok("flywheel_priority_update._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"flywheel_priority_update._dao_guard='{fpu_guard}' 未含'六飞轮'")

    # [11] review_progress_summary: stage_advances _dao_guard 含'七阶'
    print("\n[11] review_progress_summary stage_advances_since_last_review _dao_guard 含'七阶'")
    sa_guard = rps_fields.get("stage_advances_since_last_review", {}).get("_dao_guard", "")
    if "七阶" in sa_guard:
        ok("stage_advances_since_last_review._dao_guard 含'七阶' ✓")
    else:
        fail(f"stage_advances_since_last_review._dao_guard='{sa_guard}' 未含'七阶'")

    # [12] flywheel_progress_since_last_review 六飞轮 + _dao_guard
    print("\n[12] review_progress_summary flywheel_progress_since_last_review 六飞轮 + _dao_guard")
    fpslr_field = rps_fields.get("flywheel_progress_since_last_review", {})
    fpslr_props = set(fpslr_field.get("properties", {}).keys())
    if fpslr_props == VALID_FLYWHEEL_NAMES:
        ok("flywheel_progress_since_last_review 六飞轮全覆盖 ✓")
    else:
        fail(f"flywheel_progress_since_last_review {fpslr_props} ≠ {VALID_FLYWHEEL_NAMES}")
    fpslr_guard = fpslr_field.get("_dao_guard", "")
    if "六飞轮" in fpslr_guard:
        ok("flywheel_progress_since_last_review._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"flywheel_progress_since_last_review._dao_guard='{fpslr_guard}' 未含'六飞轮'")

    # [13] sop05_compliance_rate_since_last_review ⑤守护
    print("\n[13] review_progress_summary sop05_compliance_rate_since_last_review ⑤守护")
    scr_guard = rps_fields.get("sop05_compliance_rate_since_last_review", {}).get("_dao_guard", "")
    if "流程" in scr_guard:
        ok("sop05_compliance_rate_since_last_review._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_compliance_rate_since_last_review._dao_guard='{scr_guard}' 未含'流程'")

    # [14] validation_rules
    print("\n[14] validation_rules 合规")
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
        print("  ✅ 教练目标复核 schema 验证 PASS — 复核字段/⑤守护/七阶/MECE/六飞轮/PIPL 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
