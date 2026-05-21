#!/usr/bin/env python3
"""
道层家长参与 schema 验证脚本 v1.0
验证 pipeline-data/coaching-parent-engagement-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. parent_communication_types: 5种类型全覆盖
  3. 每种类型: content_scope/excluded_content/channel 非空
  4. pct-weekly _dao_guard 含'六飞轮' + 六飞轮名称枚举正确
  5. pct-milestone _dao_guard 含'七阶' + 七阶名称枚举正确
  6. parent_record_schema 核心字段 + comm_type_id enum 5个
  7. information_sharing_boundaries: theta_sharing_prohibited + _dao_guard 含'六飞轮'/'七阶'
  8. minor_parent_rules._dao_guard 含 PIPL 第14条
  9. validation_rules: 5种类型/七阶/六飞轮/sop05_guard/theta_prohibited/pipl
  10. PIPL 合规声明
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PARENT_PATH = REPO_ROOT / "pipeline-data" / "coaching-parent-engagement-schema.json"

REQUIRED_COMM_TYPE_IDS = {"pct-welcome", "pct-weekly", "pct-milestone", "pct-concern", "pct-monthly"}
VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}

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
    print("  家长参与 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not PARENT_PATH.exists():
        fail(f"找不到文件: {PARENT_PATH}")
        sys.exit(1)
    data = json.loads(PARENT_PATH.read_text(encoding="utf-8"))
    ok("coaching-parent-engagement-schema.json 加载成功")

    comm_types = data.get("parent_communication_types", [])

    # [2] 5种沟通类型全覆盖
    print("\n[2] parent_communication_types 5种类型全覆盖")
    found_ids = {c.get("comm_type_id") for c in comm_types}
    missing = REQUIRED_COMM_TYPE_IDS - found_ids
    if missing:
        fail(f"缺少沟通类型: {missing}")
    else:
        ok(f"5种沟通类型全覆盖 ✓ {sorted(found_ids)}")

    # [3] 每种类型必填字段
    print("\n[3] 每种类型必填字段")
    for c in comm_types:
        cid = c.get("comm_type_id", "?")
        if c.get("content_scope"):
            ok(f"{cid}: content_scope {len(c['content_scope'])}项 ✓")
        else:
            fail(f"{cid}: content_scope 为空")
        if c.get("excluded_content"):
            ok(f"{cid}: excluded_content {len(c['excluded_content'])}项 ✓")
        else:
            fail(f"{cid}: excluded_content 为空")
        if c.get("channel"):
            ok(f"{cid}: channel {c['channel']} ✓")
        else:
            fail(f"{cid}: channel 为空")

    # [4] pct-weekly _dao_guard 含'六飞轮'
    print("\n[4] pct-weekly 六飞轮守护")
    pct_weekly = next((c for c in comm_types if c.get("comm_type_id") == "pct-weekly"), None)
    if pct_weekly:
        guard_w = pct_weekly.get("_dao_guard", "")
        if "六飞轮" in guard_w:
            ok("pct-weekly: _dao_guard 含'六飞轮' ✓")
        else:
            fail(f"pct-weekly: _dao_guard='{guard_w}' 未含'六飞轮'")
        content_w = str(pct_weekly.get("content_scope", []))
        if "飞轮" in content_w:
            ok("pct-weekly: content_scope 提及飞轮 ✓")
        else:
            fail("pct-weekly: content_scope 未提及飞轮")
    else:
        fail("pct-weekly 类型缺失")

    # [5] pct-milestone _dao_guard 含'七阶'
    print("\n[5] pct-milestone 七阶守护")
    pct_mile = next((c for c in comm_types if c.get("comm_type_id") == "pct-milestone"), None)
    if pct_mile:
        guard_m = pct_mile.get("_dao_guard", "")
        if "七阶" in guard_m:
            ok("pct-milestone: _dao_guard 含'七阶' ✓")
        else:
            fail(f"pct-milestone: _dao_guard='{guard_m}' 未含'七阶'")
        content_m = str(pct_mile.get("content_scope", []))
        if "阶" in content_m:
            ok("pct-milestone: content_scope 提及阶位 ✓")
        else:
            fail("pct-milestone: content_scope 未提及阶位")
    else:
        fail("pct-milestone 类型缺失")

    # [6] parent_record_schema 核心字段
    print("\n[6] parent_record_schema 核心字段")
    prs = data.get("parent_record_schema", {}).get("fields", {})
    required_prs = {"comm_record_id", "student_id", "parent_id", "coach_id",
                    "comm_type_id", "sent_at", "channel_used"}
    missing_prs = required_prs - set(prs.keys())
    if missing_prs:
        fail(f"parent_record_schema 缺少字段: {missing_prs}")
    else:
        ok(f"parent_record_schema {len(prs)}个字段 核心字段全覆盖 ✓")
    ct_enum = set(prs.get("comm_type_id", {}).get("enum", []))
    if ct_enum == REQUIRED_COMM_TYPE_IDS:
        ok("comm_type_id enum 5种类型全覆盖 ✓")
    else:
        fail(f"comm_type_id enum {ct_enum} ≠ {REQUIRED_COMM_TYPE_IDS}")

    # [7] information_sharing_boundaries
    print("\n[7] information_sharing_boundaries θ 禁止/六飞轮/七阶")
    isb = data.get("information_sharing_boundaries", {})
    prohibited = isb.get("prohibited_to_share", [])
    if any("theta" in p.lower() for p in prohibited):
        ok("information_sharing_boundaries 禁止分享 θ 值 ✓")
    else:
        fail("information_sharing_boundaries 未明确禁止分享 θ 值")
    allowed = isb.get("allowed_to_share", [])
    if any("七阶" in a or "stage" in a.lower() for a in allowed):
        ok("information_sharing_boundaries 允许分享七阶等级名称 ✓")
    else:
        fail("information_sharing_boundaries 未说明可分享七阶等级名称")
    isb_guard = isb.get("_dao_guard", "")
    if "六飞轮" in isb_guard and "七阶" in isb_guard:
        ok("information_sharing_boundaries._dao_guard 含'六飞轮'+'七阶' ✓")
    else:
        fail(f"information_sharing_boundaries._dao_guard='{isb_guard}' 不完整")

    # [8] minor_parent_rules PIPL 第14条
    print("\n[8] minor_parent_rules PIPL 第14条守护")
    mpr = data.get("minor_parent_rules", {})
    mpr_guard = mpr.get("_dao_guard", "")
    if "PIPL" in mpr_guard and "14" in mpr_guard:
        ok("minor_parent_rules._dao_guard 含 PIPL 第14条 ✓")
    else:
        fail(f"minor_parent_rules._dao_guard='{mpr_guard}' 未含 PIPL 第14条")
    if mpr.get("mandatory_for_under14"):
        ok(f"minor_parent_rules.mandatory_for_under14 {len(mpr['mandatory_for_under14'])}条 ✓")
    else:
        fail("minor_parent_rules.mandatory_for_under14 为空")
    pipl14_constraint = mpr.get("pipl_constraint", "")
    if "PIPL" in pipl14_constraint and "14" in pipl14_constraint:
        ok("minor_parent_rules.pipl_constraint 存在 ✓")
    else:
        fail("minor_parent_rules.pipl_constraint 缺失")

    # [9] validation_rules
    print("\n[9] validation_rules 合规")
    vr = data.get("validation_rules", {})
    ct_count = vr.get("comm_types_count", 0)
    if ct_count == 5:
        ok("validation_rules.comm_types_count=5 ✓")
    else:
        fail(f"validation_rules.comm_types_count={ct_count} ≠ 5")

    fw_names = set(vr.get("six_flywheel_valid_names", []))
    if fw_names == VALID_FLYWHEEL_NAMES:
        ok("validation_rules.six_flywheel_valid_names 六飞轮全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names {fw_names} ≠ {VALID_FLYWHEEL_NAMES}")

    stage_names = set(vr.get("seven_stage_valid_names", []))
    if stage_names == VALID_STAGE_NAMES:
        ok("validation_rules.seven_stage_valid_names 七阶全覆盖 ✓")
    else:
        fail(f"seven_stage_valid_names {stage_names} ≠ {VALID_STAGE_NAMES}")

    theta_prohibited = vr.get("theta_sharing_prohibited", False)
    if theta_prohibited is True:
        ok("validation_rules.theta_sharing_prohibited=true ✓")
    else:
        fail("validation_rules.theta_sharing_prohibited 未设为 true")

    sop05_guard = vr.get("sop05_guard", "")
    if "流程" in sop05_guard:
        ok("validation_rules.sop05_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"validation_rules.sop05_guard='{sop05_guard}' 未含'流程'")

    ct_ids = set(vr.get("comm_type_ids", []))
    if ct_ids == REQUIRED_COMM_TYPE_IDS:
        ok("validation_rules.comm_type_ids 5种类型 ✓")
    else:
        fail(f"validation_rules.comm_type_ids {ct_ids} ≠ {REQUIRED_COMM_TYPE_IDS}")

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
        print("  ✅ 家长参与 schema 验证 PASS — 5类沟通/六飞轮/七阶/PIPL 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
