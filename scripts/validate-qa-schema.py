#!/usr/bin/env python3
"""
道层教练质量保证 schema 验证脚本 v1.0
验证 pipeline-data/coaching-qa-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. qa_dimensions: 5个维度全覆盖 + 权重之和 == 1.0
  3. qa-d1 含 ⑤第5步=流程 守护
  4. qa_review_types: 4类评审全覆盖
  5. qa_score_schema 核心字段完整
  6. dimension_scores 5个维度字段
  7. qa_thresholds 合规
  8. validation_rules step_id_5_name='流程' + six_flywheel_valid_names 6个
  9. PIPL 合规声明
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
QA_PATH = REPO_ROOT / "pipeline-data" / "coaching-qa-schema.json"

REQUIRED_DIM_IDS = {"qa-d1", "qa-d2", "qa-d3", "qa-d4", "qa-d5"}
REQUIRED_REVIEW_TYPE_IDS = {"qar-self", "qar-peer", "qar-supervisor", "qar-calibration"}
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
    print("  教练质量保证 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not QA_PATH.exists():
        fail(f"找不到文件: {QA_PATH}")
        sys.exit(1)
    data = json.loads(QA_PATH.read_text(encoding="utf-8"))
    ok("coaching-qa-schema.json 加载成功")

    dims = data.get("qa_dimensions", [])
    review_types = data.get("qa_review_types", [])

    # [2] 5个维度 + 权重之和
    print("\n[2] qa_dimensions 5维度 + 权重归一")
    found_dim_ids = {d.get("dimension_id") for d in dims}
    missing_dims = REQUIRED_DIM_IDS - found_dim_ids
    if missing_dims:
        fail(f"缺少维度: {missing_dims}")
    else:
        ok(f"5个维度全覆盖 ✓ {sorted(found_dim_ids)}")

    total_weight = sum(d.get("weight", 0) for d in dims)
    if abs(total_weight - 1.0) < 1e-9:
        ok(f"权重之和 = {total_weight:.2f} == 1.0 ✓")
    else:
        fail(f"权重之和 = {total_weight:.4f} ≠ 1.0")

    for d in dims:
        did = d.get("dimension_id", "?")
        w = d.get("weight", 0)
        criteria = d.get("evaluation_criteria", [])
        if criteria:
            ok(f"{did}: evaluation_criteria {len(criteria)}条 ✓")
        else:
            fail(f"{did}: evaluation_criteria 为空")
        if 0 < w < 1:
            ok(f"{did}: weight={w} ∈ (0,1) ✓")
        else:
            fail(f"{did}: weight={w} 超出 (0,1)")

    # [3] qa-d1 ⑤守护
    print("\n[3] ⑤守护验证 (qa-d1)")
    qa_d1 = next((d for d in dims if d.get("dimension_id") == "qa-d1"), None)
    if qa_d1 is None:
        fail("qa-d1 维度缺失")
    else:
        guard = qa_d1.get("_dao_guard", "")
        if "流程" in guard:
            ok("qa-d1: _dao_guard 含'流程' ⑤守护 ✓")
        else:
            fail(f"qa-d1: _dao_guard='{guard}' 未含'流程'")
        # Check evaluation_criteria for 流程
        criteria_text = str(qa_d1.get("evaluation_criteria", []))
        if "流程" in criteria_text:
            ok("qa-d1: evaluation_criteria 提及'流程' ✓")
        else:
            fail("qa-d1: evaluation_criteria 未提及'流程'")

    # [4] 4类评审全覆盖
    print("\n[4] qa_review_types 4类评审全覆盖")
    found_rtype_ids = {r.get("review_type_id") for r in review_types}
    missing_rtypes = REQUIRED_REVIEW_TYPE_IDS - found_rtype_ids
    if missing_rtypes:
        fail(f"缺少评审类型: {missing_rtypes}")
    else:
        ok(f"4类评审全覆盖 ✓ {sorted(found_rtype_ids)}")

    for r in review_types:
        rtid = r.get("review_type_id", "?")
        dims_covered = r.get("dimensions_covered", [])
        dur = r.get("duration_min", 0)
        if dims_covered:
            ok(f"{rtid}: dimensions_covered {len(dims_covered)}个 ✓")
        else:
            fail(f"{rtid}: dimensions_covered 为空")
        if dur > 0:
            ok(f"{rtid}: duration_min={dur}分 ✓")
        else:
            fail(f"{rtid}: duration_min={dur} ≤ 0")

    # [5] qa_score_schema 核心字段
    print("\n[5] qa_score_schema 核心字段")
    schema_fields = data.get("qa_score_schema", {}).get("fields", {})
    required_fields = {"qa_record_id", "session_id", "coach_id", "reviewer_id",
                       "review_type", "dimension_scores", "weighted_score", "sop05_compliance"}
    missing_sf = required_fields - set(schema_fields.keys())
    if missing_sf:
        fail(f"qa_score_schema 缺少字段: {missing_sf}")
    else:
        ok(f"qa_score_schema {len(schema_fields)}个字段 核心字段全覆盖 ✓")

    # review_type enum
    rt_enum = set(schema_fields.get("review_type", {}).get("enum", []))
    if rt_enum == REQUIRED_REVIEW_TYPE_IDS:
        ok(f"review_type enum 4类全覆盖 ✓")
    else:
        fail(f"review_type enum {rt_enum} ≠ {REQUIRED_REVIEW_TYPE_IDS}")

    # [6] dimension_scores 5个维度
    print("\n[6] dimension_scores 5维度字段")
    ds_props = schema_fields.get("dimension_scores", {}).get("properties", {})
    missing_ds = REQUIRED_DIM_IDS - set(ds_props.keys())
    if missing_ds:
        fail(f"dimension_scores 缺少维度: {missing_ds}")
    else:
        ok(f"dimension_scores 5维度字段全覆盖 ✓")
    for dk, dv in ds_props.items():
        dmin = dv.get("minimum", 0)
        dmax = dv.get("maximum", 0)
        if dmin == 1 and dmax == 10:
            ok(f"dimension_scores.{dk}: range [1,10] ✓")
        else:
            fail(f"dimension_scores.{dk}: range [{dmin},{dmax}] ≠ [1,10]")

    # [7] qa_thresholds
    print("\n[7] qa_thresholds 合规")
    qt = data.get("qa_thresholds", {})
    min_sess = qt.get("min_weighted_score_per_session", 0)
    min_month = qt.get("min_monthly_avg_score", 0)
    sop05_rate = qt.get("sop05_compliance_rate_target", 0)
    if min_sess > 0:
        ok(f"min_weighted_score_per_session={min_sess} > 0 ✓")
    else:
        fail(f"min_weighted_score_per_session={min_sess} ≤ 0")
    if min_month >= min_sess:
        ok(f"min_monthly_avg_score={min_month} ≥ per_session={min_sess} ✓")
    else:
        fail(f"min_monthly_avg_score={min_month} < per_session={min_sess}")
    if sop05_rate == 1.0:
        ok(f"sop05_compliance_rate_target={sop05_rate} = 1.0 (完全合规) ✓")
    else:
        fail(f"sop05_compliance_rate_target={sop05_rate} ≠ 1.0")

    # [8] validation_rules
    print("\n[8] validation_rules 合规")
    vr = data.get("validation_rules", {})
    step5_name = vr.get("eight_step_name_constraints", {}).get("step_id_5_name", "")
    if step5_name == "流程":
        ok("validation_rules step_id_5_name='流程' ⑤联动守护 ✓")
    else:
        fail(f"validation_rules step_id_5_name='{step5_name}' ≠ '流程'")

    fw_names = set(vr.get("six_flywheel_valid_names", []))
    missing_fw = VALID_FLYWHEEL_NAMES - fw_names
    if missing_fw:
        fail(f"six_flywheel_valid_names 缺少: {missing_fw}")
    elif len(fw_names) == 6:
        ok("six_flywheel_valid_names 六飞轮全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names 数量 {len(fw_names)} ≠ 6")

    wsc = vr.get("weight_sum_constraint", "")
    if "1.0" in wsc:
        ok("weight_sum_constraint 存在 ✓")
    else:
        fail("weight_sum_constraint 缺失或未含 1.0")

    # [9] PIPL 合规
    print("\n[9] PIPL 合规")
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
        print("  ✅ 教练质量保证 schema 验证 PASS — 5维度×4类评审全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
