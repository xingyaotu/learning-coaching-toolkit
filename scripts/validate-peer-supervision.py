#!/usr/bin/env python3
"""
道层教练同伴督导 schema 验证脚本 v1.0
验证 pipeline-data/coaching-peer-supervision-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. supervision_pair_schema 核心字段完整性
  3. supervision_session_schema 核心字段: 10个必填
  4. sop_compliance_review 含 _dao_guard + '流程' — ⑤守护
  5. dimension_scores_given 5个 QA 维度 [1,10]
  6. flywheel_coaching_review 六飞轮枚举
  7. supervision_cycle_schema: sop05_compliance_rate 字段存在
  8. pairing_rules: sop05_review_mandatory=true + _dao_guard 含'流程'
  9. validation_rules: 5个 QA 维度/六飞轮/sop05_guard/pipl
  10. PIPL 合规声明
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SUPERVISION_PATH = REPO_ROOT / "pipeline-data" / "coaching-peer-supervision-schema.json"

VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_QA_DIMS = {"qa-d1", "qa-d2", "qa-d3", "qa-d4", "qa-d5"}
REQUIRED_SESSION_FIELDS = {
    "supervision_id", "pair_id", "supervisee_id", "supervisor_id",
    "supervision_date", "duration_min", "review_type_id",
    "focus_dimensions", "sop_compliance_review", "dimension_scores_given"
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
    print("  教练同伴督导 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not SUPERVISION_PATH.exists():
        fail(f"找不到文件: {SUPERVISION_PATH}")
        sys.exit(1)
    data = json.loads(SUPERVISION_PATH.read_text(encoding="utf-8"))
    ok("coaching-peer-supervision-schema.json 加载成功")

    pair_schema = data.get("supervision_pair_schema", {}).get("fields", {})
    sess_schema = data.get("supervision_session_schema", {}).get("fields", {})
    cycle_schema = data.get("supervision_cycle_schema", {}).get("fields", {})

    # [2] supervision_pair_schema 核心字段
    print("\n[2] supervision_pair_schema 配对字段")
    required_pair = {"pair_id", "coach_a_id", "coach_b_id", "pair_start_date", "rotation_period_months"}
    missing_pair = required_pair - set(pair_schema.keys())
    if missing_pair:
        fail(f"supervision_pair_schema 缺少字段: {missing_pair}")
    else:
        ok(f"supervision_pair_schema {len(pair_schema)}个字段 核心字段全覆盖 ✓")

    # shared_focus_dimensions enum
    sfd_enum = set(pair_schema.get("shared_focus_dimensions", {}).get("items", {}).get("enum", []))
    if sfd_enum == VALID_QA_DIMS:
        ok("supervision_pair.shared_focus_dimensions enum 5个 QA 维度 ✓")
    else:
        fail(f"shared_focus_dimensions enum {sfd_enum} ≠ {VALID_QA_DIMS}")

    # [3] supervision_session_schema 核心字段
    print("\n[3] supervision_session_schema 10个必填字段")
    vr_sess = set(data.get("validation_rules", {}).get("supervision_session_required_fields", []))
    if vr_sess == REQUIRED_SESSION_FIELDS:
        ok(f"validation_rules.supervision_session_required_fields 10字段全覆盖 ✓")
    else:
        missing_sf = REQUIRED_SESSION_FIELDS - vr_sess
        extra_sf = vr_sess - REQUIRED_SESSION_FIELDS
        if missing_sf:
            fail(f"supervision_session_required_fields 缺少: {missing_sf}")
        if extra_sf:
            ok(f"supervision_session_required_fields 含额外字段: {extra_sf}")

    for fname in REQUIRED_SESSION_FIELDS:
        if fname in sess_schema:
            ok(f"supervision_session_schema.fields.{fname} 存在 ✓")
        else:
            fail(f"supervision_session_schema.fields.{fname} 缺失")

    # [4] sop_compliance_review _dao_guard + '流程'
    print("\n[4] ⑤守护 — sop_compliance_review _dao_guard 含'流程'")
    scr = sess_schema.get("sop_compliance_review", {}).get("properties", {})
    scr_guard = sess_schema.get("sop_compliance_review", {}).get("properties", {})
    # Check _dao_guard inside sop_compliance_review
    sop_review_field = sess_schema.get("sop_compliance_review", {})
    scr_all = str(sop_review_field)
    if "流程" in scr_all:
        ok("sop_compliance_review 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop_compliance_review 未含'流程'")
    if "_dao_guard" in scr_all:
        ok("sop_compliance_review._dao_guard 存在 ✓")
    else:
        fail("sop_compliance_review._dao_guard 缺失")

    scr_props = sop_review_field.get("properties", {})
    for required_scr_field in ["sop05_sessions_reviewed", "sop05_compliant_count", "correction_agreed"]:
        if required_scr_field in scr_props:
            ok(f"sop_compliance_review.{required_scr_field} 存在 ✓")
        else:
            fail(f"sop_compliance_review.{required_scr_field} 缺失")

    # [5] dimension_scores_given 5个 QA 维度 [1,10]
    print("\n[5] dimension_scores_given 5维度 [1,10]")
    dsg = sess_schema.get("dimension_scores_given", {}).get("properties", {})
    missing_dsg = VALID_QA_DIMS - set(dsg.keys())
    if missing_dsg:
        fail(f"dimension_scores_given 缺少维度: {missing_dsg}")
    else:
        ok(f"dimension_scores_given 5维度全覆盖 ✓")
    for dk, dv in dsg.items():
        dmin = dv.get("minimum", 0)
        dmax = dv.get("maximum", 0)
        if dmin == 1 and dmax == 10:
            ok(f"dimension_scores_given.{dk}: range [1,10] ✓")
        else:
            fail(f"dimension_scores_given.{dk}: range [{dmin},{dmax}] ≠ [1,10]")

    # [6] flywheel_coaching_review 六飞轮枚举
    print("\n[6] flywheel_coaching_review 六飞轮枚举")
    fcr = sess_schema.get("flywheel_coaching_review", {}).get("properties", {})
    fd_enum = set(fcr.get("flywheels_discussed", {}).get("items", {}).get("enum", []))
    missing_fw = VALID_FLYWHEEL_NAMES - fd_enum
    if missing_fw:
        fail(f"flywheels_discussed enum 缺少: {missing_fw}")
    elif len(fd_enum) == 6:
        ok("flywheel_coaching_review.flywheels_discussed enum 六飞轮全覆盖 ✓")
    else:
        fail(f"flywheels_discussed enum 数量 {len(fd_enum)} ≠ 6")

    # [7] supervision_cycle_schema
    print("\n[7] supervision_cycle_schema 周期汇总")
    if "sop05_compliance_rate_this_cycle" in cycle_schema:
        ok("supervision_cycle_schema.sop05_compliance_rate_this_cycle 存在 ✓")
    else:
        fail("supervision_cycle_schema.sop05_compliance_rate_this_cycle 缺失")
    sop05_cr = cycle_schema.get("sop05_compliance_rate_this_cycle", {})
    if sop05_cr.get("minimum") == 0 and sop05_cr.get("maximum") == 1:
        ok("sop05_compliance_rate_this_cycle range [0,1] ✓")
    else:
        fail(f"sop05_compliance_rate_this_cycle range [{sop05_cr.get('minimum')},{sop05_cr.get('maximum')}] ≠ [0,1]")

    # [8] pairing_rules
    print("\n[8] pairing_rules sop05_review_mandatory + _dao_guard 含'流程'")
    pr = data.get("pairing_rules", {})
    if pr.get("sop05_review_mandatory") is True:
        ok("pairing_rules.sop05_review_mandatory=true ✓")
    else:
        fail(f"pairing_rules.sop05_review_mandatory={pr.get('sop05_review_mandatory')} ≠ true")
    pr_guard = pr.get("_dao_guard", "")
    if "流程" in pr_guard:
        ok("pairing_rules._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"pairing_rules._dao_guard='{pr_guard}' 未含'流程'")
    rot = pr.get("rotation_period_default_months", 0)
    if 1 <= rot <= 6:
        ok(f"pairing_rules.rotation_period_default_months={rot} ∈ [1,6] ✓")
    else:
        fail(f"pairing_rules.rotation_period_default_months={rot} 超出 [1,6]")

    # [9] validation_rules
    print("\n[9] validation_rules 合规")
    vr = data.get("validation_rules", {})
    five_dims = set(vr.get("five_qa_dimensions", []))
    if five_dims == VALID_QA_DIMS:
        ok("validation_rules.five_qa_dimensions 5维度 ✓")
    else:
        fail(f"validation_rules.five_qa_dimensions {five_dims} ≠ {VALID_QA_DIMS}")

    fw_names = set(vr.get("six_flywheel_valid_names", []))
    missing_fw_vr = VALID_FLYWHEEL_NAMES - fw_names
    if missing_fw_vr:
        fail(f"validation_rules.six_flywheel_valid_names 缺少: {missing_fw_vr}")
    elif len(fw_names) == 6:
        ok("validation_rules.six_flywheel_valid_names 六飞轮全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names 数量 {len(fw_names)} ≠ 6")

    sop05_guard_vr = vr.get("sop05_compliance_guard", "")
    if "流程" in sop05_guard_vr:
        ok("validation_rules.sop05_compliance_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"validation_rules.sop05_compliance_guard='{sop05_guard_vr}' 未含'流程'")

    dur_thr = vr.get("duration_min_threshold", 0)
    if dur_thr >= 20:
        ok(f"validation_rules.duration_min_threshold={dur_thr} ≥ 20 ✓")
    else:
        fail(f"validation_rules.duration_min_threshold={dur_thr} < 20")

    rt_must = vr.get("review_type_must_be", "")
    if rt_must == "qar-peer":
        ok("validation_rules.review_type_must_be='qar-peer' ✓")
    else:
        fail(f"validation_rules.review_type_must_be='{rt_must}' ≠ 'qar-peer'")

    # [10] PIPL 合规
    print("\n[10] PIPL 合规")
    pipl_meta = data.get("_meta", {}).get("pipl_note", "")
    if "PIPL" in pipl_meta and "匿名" in pipl_meta:
        ok("_meta.pipl_note PIPL 合规声明 ✓")
    else:
        fail("_meta.pipl_note 缺少 PIPL 合规声明")
    pipl_vr = vr.get("pipl_constraints", "")
    if "PIPL" in pipl_vr or "匿名" in pipl_vr:
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
        print("  ✅ 教练同伴督导 schema 验证 PASS — 配对规则/⑤守护/飞轮/PIPL 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
