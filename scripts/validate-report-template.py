#!/usr/bin/env python3
"""
道层教练报告模板 schema 验证脚本 v1.0
验证 pipeline-data/coaching-report-template-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. 6类报告全覆盖 (session_summary/weekly_progress/milestone_review/monthly_summary/goal_completion/hq_analytics)
  3. 每类报告 target_portals 非空
  4. 每类报告 sections 非空，且每个 section 有 required_fields
  5. flywheel_enum_guard 值在六飞轮枚举内
  6. ⑤守护: milestone_review 含 five_step_guard 字段
  7. portal_access_control 四门户覆盖 (student/parent/coach/hq)
  8. hq_analytics 仅 hq 可访问
  9. dao_layer_guards step_id_5_name='流程'
  10. validation_rules six_flywheel_valid_names 6个
  11. PIPL 合规声明
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
REPORT_TPL_PATH = REPO_ROOT / "pipeline-data" / "coaching-report-template-schema.json"

REQUIRED_REPORT_TYPE_IDS = {
    "session_summary", "weekly_progress", "milestone_review",
    "monthly_summary", "goal_completion", "hq_analytics"
}
REQUIRED_PORTALS = {"student", "parent", "coach", "hq"}
VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}

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
    print("  教练报告模板 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not REPORT_TPL_PATH.exists():
        fail(f"找不到文件: {REPORT_TPL_PATH}")
        sys.exit(1)
    data = json.loads(REPORT_TPL_PATH.read_text(encoding="utf-8"))
    ok("coaching-report-template-schema.json 加载成功")

    report_types = data.get("report_types", [])

    # [2] 6类报告全覆盖
    print("\n[2] 6类报告全覆盖")
    found_rtype_ids = {r.get("report_type_id") for r in report_types}
    missing_types = REQUIRED_REPORT_TYPE_IDS - found_rtype_ids
    if missing_types:
        fail(f"缺少报告类型: {missing_types}")
    else:
        ok(f"6类报告全覆盖 ✓ {sorted(found_rtype_ids)}")

    milestone_report = None
    five_step_guarded = False

    # [3-5] 逐报告类型验证
    print("\n[3-5] 逐报告类型验证")
    for r in report_types:
        rtid = r.get("report_type_id", "?")
        rtname = r.get("report_type_name", "?")
        label = f"{rtid}"

        # [3] target_portals 非空
        portals = r.get("target_portals", [])
        if portals:
            ok(f"{label}: target_portals {portals} ✓")
        else:
            fail(f"{label}: target_portals 为空")

        # [4] sections 非空
        sections = r.get("sections", [])
        if sections:
            ok(f"{label}: {len(sections)}个 section ✓")
        else:
            fail(f"{label}: sections 为空")

        for s in sections:
            sid = s.get("section_id", "?")
            rf = s.get("required_fields", [])
            if rf:
                ok(f"{label}/{sid}: required_fields {len(rf)}个 ✓")
            else:
                fail(f"{label}/{sid}: required_fields 为空")

            # [5] flywheel_enum_guard 合规
            fw_guard = s.get("flywheel_enum_guard", [])
            if fw_guard:
                invalid_fw = set(fw_guard) - VALID_FLYWHEEL_NAMES
                if invalid_fw:
                    fail(f"{label}/{sid}: flywheel_enum_guard 含非法飞轮 {invalid_fw}")
                elif len(fw_guard) == 6:
                    ok(f"{label}/{sid}: flywheel_enum_guard 六飞轮全覆盖 ✓")
                else:
                    ok(f"{label}/{sid}: flywheel_enum_guard {fw_guard} 合规 ✓")

            # ⑤守护检测
            fsg = s.get("five_step_guard", "")
            if fsg:
                five_step_guarded = True
                if "流程" in fsg:
                    ok(f"{label}/{sid}: five_step_guard 含'流程' ✓")
                else:
                    fail(f"{label}/{sid}: five_step_guard='{fsg}' 未含'流程'")

        if rtid == "milestone_review":
            milestone_report = r

    # [6] ⑤守护
    print("\n[6] ⑤守护验证")
    if milestone_report is None:
        fail("milestone_review 报告类型缺失")
    elif not five_step_guarded:
        fail("milestone_review 中缺少 five_step_guard 字段")
    else:
        ok("milestone_review five_step_guard ⑤联动守护 ✓")

    # dao_layer_guards ⑤守护
    dlg = data.get("dao_layer_guards", {})
    dao_guard5 = dlg.get("_dao_guard_five", "")
    if "流程" in dao_guard5:
        ok("dao_layer_guards._dao_guard_five 含'流程' ⑤守护 ✓")
    else:
        fail(f"dao_layer_guards._dao_guard_five='{dao_guard5}' 未含'流程'")
    step5_dlg = dlg.get("eight_step_name_constraints", {}).get("step_id_5_name", "")
    if step5_dlg == "流程":
        ok("dao_layer_guards step_id_5_name='流程' ✓")
    else:
        fail(f"dao_layer_guards step_id_5_name='{step5_dlg}' ≠ '流程'")

    # [7] portal_access_control 四门户覆盖
    print("\n[7] portal_access_control 四门户覆盖")
    pac = data.get("portal_access_control", {})
    found_portals = set(pac.keys())
    missing_portals = REQUIRED_PORTALS - found_portals
    if missing_portals:
        fail(f"portal_access_control 缺少门户: {missing_portals}")
    else:
        ok(f"四门户全覆盖 ✓ {sorted(found_portals)}")
    for portal, rtypes in pac.items():
        if rtypes:
            ok(f"portal.{portal}: {len(rtypes)}种报告访问权 ✓")
        else:
            fail(f"portal.{portal}: 报告访问权为空")

    # [8] hq_analytics 仅 hq 可访问
    print("\n[8] hq_analytics 访问控制")
    for portal, rtypes in pac.items():
        if portal != "hq" and "hq_analytics" in rtypes:
            fail(f"portal.{portal} 不应有 hq_analytics 访问权")
    if "hq_analytics" in pac.get("hq", []):
        ok("hq_analytics 仅 hq 可访问 ✓")
    else:
        fail("hq portal 缺少 hq_analytics 访问权")

    # [9] validation_rules step_id_5_name
    print("\n[9] validation_rules ⑤守护")
    vr = data.get("validation_rules", {})
    step5_vr = vr.get("eight_step_name_constraints", {}).get("step_id_5_name", "")
    if step5_vr == "流程":
        ok("validation_rules step_id_5_name='流程' ⑤联动守护 ✓")
    else:
        fail(f"validation_rules step_id_5_name='{step5_vr}' ≠ '流程'")

    # [10] six_flywheel_valid_names
    print("\n[10] six_flywheel_valid_names 枚举")
    fw_names = set(vr.get("six_flywheel_valid_names", []))
    missing_fw = VALID_FLYWHEEL_NAMES - fw_names
    if missing_fw:
        fail(f"six_flywheel_valid_names 缺少: {missing_fw}")
    elif len(fw_names) == 6:
        ok("six_flywheel_valid_names 六飞轮全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names 数量 {len(fw_names)} ≠ 6")

    # [11] PIPL 合规
    print("\n[11] PIPL 合规")
    pipl_meta = data.get("_meta", {}).get("pipl_note", "")
    if "PIPL" in pipl_meta and "匿名" in pipl_meta:
        ok("_meta.pipl_note PIPL 合规声明存在 ✓")
    else:
        fail("_meta.pipl_note 缺少 PIPL 合规声明")
    pipl_vr = vr.get("pipl_constraints", "")
    if "匿名" in pipl_vr or "PIPL" in pipl_vr:
        ok("validation_rules.pipl_constraints 存在 ✓")
    else:
        fail("validation_rules.pipl_constraints 缺失")

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
        print("  ✅ 教练报告模板 schema 验证 PASS — 6类报告×4门户全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
