#!/usr/bin/env python3
"""
道层教练认证等级 schema 验证脚本 v1.0
验证 pipeline-data/coaching-certification-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. certification_levels: 5个等级全覆盖 + rank 1-5 递增
  3. 每个等级: entry_requirements/competency_standards/privileges/_dao_guard 非空
  4. sop05_compliance_rate_min 递增 0.70→0.85→0.92→0.95→0.98
  5. 每个等级 _dao_guard 含'流程' — ⑤守护
  6. dao_layer_exam_content 含六飞轮/七阶/'流程' 考点
  7. certification_record_schema 核心字段 + level_id enum 5个
  8. validation_rules: 5个等级/sop05_guard 含'流程'/六飞轮/七阶/pipl
  9. PIPL 合规声明
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CERT_PATH = REPO_ROOT / "pipeline-data" / "coaching-certification-schema.json"

REQUIRED_LEVEL_IDS = {"ccl-1", "ccl-2", "ccl-3", "ccl-4", "ccl-5"}
VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}
EXPECTED_SOP05_RATES = {
    "ccl-1": 0.70, "ccl-2": 0.85, "ccl-3": 0.92, "ccl-4": 0.95, "ccl-5": 0.98
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
    print("  教练认证等级 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not CERT_PATH.exists():
        fail(f"找不到文件: {CERT_PATH}")
        sys.exit(1)
    data = json.loads(CERT_PATH.read_text(encoding="utf-8"))
    ok("coaching-certification-schema.json 加载成功")

    levels = data.get("certification_levels", [])

    # [2] 5个等级 + rank 1-5 递增
    print("\n[2] certification_levels 5等级 + rank 递增")
    found_ids = {lv.get("level_id") for lv in levels}
    missing = REQUIRED_LEVEL_IDS - found_ids
    if missing:
        fail(f"缺少认证等级: {missing}")
    else:
        ok(f"5个认证等级全覆盖 ✓ {sorted(found_ids)}")

    ranks = [lv.get("rank", 0) for lv in sorted(levels, key=lambda x: x.get("level_id", ""))]
    if ranks == sorted(ranks) and len(set(ranks)) == len(ranks):
        ok(f"rank 递增 {ranks} ✓")
    else:
        fail(f"rank 非严格递增: {ranks}")

    # [3] 每个等级必填字段
    print("\n[3] 每个等级必填字段")
    for lv in levels:
        lid = lv.get("level_id", "?")
        er = lv.get("entry_requirements", {})
        cs = lv.get("competency_standards", {})
        priv = lv.get("privileges", [])
        guard = lv.get("_dao_guard", "")
        if er:
            ok(f"{lid}: entry_requirements {len(er)}项 ✓")
        else:
            fail(f"{lid}: entry_requirements 为空")
        if cs:
            ok(f"{lid}: competency_standards {len(cs)}项 ✓")
        else:
            fail(f"{lid}: competency_standards 为空")
        if priv:
            ok(f"{lid}: privileges {len(priv)}项 ✓")
        else:
            fail(f"{lid}: privileges 为空")
        if guard:
            ok(f"{lid}: _dao_guard 存在 ✓")
        else:
            fail(f"{lid}: _dao_guard 缺失")

    # [4] sop05_compliance_rate_min 递增
    print("\n[4] sop05_compliance_rate_min 递增 0.70→0.85→0.92→0.95→0.98")
    prev_rate = 0.0
    sorted_levels = sorted(levels, key=lambda x: x.get("rank", 0))
    for lv in sorted_levels:
        lid = lv.get("level_id", "?")
        rate = lv.get("competency_standards", {}).get("sop05_compliance_rate_min", 0)
        expected = EXPECTED_SOP05_RATES.get(lid, 0)
        if rate == expected:
            ok(f"{lid}: sop05_compliance_rate_min={rate} = {expected} ✓")
        else:
            fail(f"{lid}: sop05_compliance_rate_min={rate} ≠ {expected}")
        if rate > prev_rate:
            ok(f"{lid}: rate {rate} > prev {prev_rate} (递增) ✓")
        else:
            fail(f"{lid}: rate {rate} ≤ prev {prev_rate} (未递增)")
        prev_rate = rate

    # [5] 每个等级 _dao_guard 含'流程'
    print("\n[5] ⑤守护 — 每个等级 _dao_guard 含'流程'")
    for lv in levels:
        lid = lv.get("level_id", "?")
        guard = lv.get("_dao_guard", "")
        if "流程" in guard:
            ok(f"{lid}: _dao_guard 含'流程' ⑤守护 ✓")
        else:
            fail(f"{lid}: _dao_guard='{guard}' 未含'流程'")

    # [6] dao_layer_exam_content
    print("\n[6] dao_layer_exam_content 道层考试内容")
    dlec = data.get("dao_layer_exam_content", {})
    topics = dlec.get("topics", [])
    topics_str = str(topics)
    if "流程" in topics_str:
        ok("dao_layer_exam_content 考点含'流程' ✓")
    else:
        fail("dao_layer_exam_content 考点未含'流程'")
    if "六飞轮" in topics_str or "计划" in topics_str:
        ok("dao_layer_exam_content 考点含六飞轮 ✓")
    else:
        fail("dao_layer_exam_content 考点未含六飞轮")
    if "七阶" in topics_str:
        ok("dao_layer_exam_content 考点含七阶 ✓")
    else:
        fail("dao_layer_exam_content 考点未含七阶")
    passing = dlec.get("passing_score", 0)
    if passing >= 80:
        ok(f"dao_layer_exam passing_score={passing} ≥ 80 ✓")
    else:
        fail(f"dao_layer_exam passing_score={passing} < 80")
    dlec_guard = dlec.get("_dao_guard", "")
    if "流程" in dlec_guard:
        ok("dao_layer_exam_content._dao_guard 含'流程' ✓")
    else:
        fail(f"dao_layer_exam_content._dao_guard='{dlec_guard}' 未含'流程'")

    # [7] certification_record_schema
    print("\n[7] certification_record_schema 核心字段")
    crs_fields = data.get("certification_record_schema", {}).get("fields", {})
    required_crs = {"cert_id", "coach_id", "level_id", "certified_at", "expires_at",
                    "sop05_compliance_rate_at_cert", "dao_layer_exam_score", "status"}
    missing_crs = required_crs - set(crs_fields.keys())
    if missing_crs:
        fail(f"certification_record_schema 缺少字段: {missing_crs}")
    else:
        ok(f"certification_record_schema {len(crs_fields)}个字段 核心字段全覆盖 ✓")

    level_enum = set(crs_fields.get("level_id", {}).get("enum", []))
    if level_enum == REQUIRED_LEVEL_IDS:
        ok("level_id enum 5个等级全覆盖 ✓")
    else:
        fail(f"level_id enum {level_enum} ≠ {REQUIRED_LEVEL_IDS}")

    status_enum = set(crs_fields.get("status", {}).get("enum", []))
    if status_enum:
        ok(f"status enum {len(status_enum)}个选项 ✓")
    else:
        fail("status enum 为空")

    # [8] validation_rules
    print("\n[8] validation_rules 合规")
    vr = data.get("validation_rules", {})
    lc = vr.get("certification_levels_count", 0)
    if lc == 5:
        ok("validation_rules.certification_levels_count=5 ✓")
    else:
        fail(f"validation_rules.certification_levels_count={lc} ≠ 5")

    five_ids = set(vr.get("five_level_ids", []))
    if five_ids == REQUIRED_LEVEL_IDS:
        ok("validation_rules.five_level_ids 5个等级 ✓")
    else:
        fail(f"validation_rules.five_level_ids {five_ids} ≠ {REQUIRED_LEVEL_IDS}")

    sop05_guard = vr.get("sop05_guard", "")
    if "流程" in sop05_guard:
        ok("validation_rules.sop05_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"validation_rules.sop05_guard='{sop05_guard}' 未含'流程'")

    fw_names = set(vr.get("six_flywheel_valid_names", []))
    missing_fw = VALID_FLYWHEEL_NAMES - fw_names
    if missing_fw:
        fail(f"six_flywheel_valid_names 缺少: {missing_fw}")
    elif len(fw_names) == 6:
        ok("validation_rules.six_flywheel_valid_names 六飞轮全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names 数量 {len(fw_names)} ≠ 6")

    stage_names = set(vr.get("seven_stage_valid_names", []))
    missing_st = VALID_STAGE_NAMES - stage_names
    if missing_st:
        fail(f"seven_stage_valid_names 缺少: {missing_st}")
    elif len(stage_names) == 7:
        ok("validation_rules.seven_stage_valid_names 七阶全覆盖 ✓")
    else:
        fail(f"seven_stage_valid_names 数量 {len(stage_names)} ≠ 7")

    dao_mandatory = vr.get("dao_layer_exam_mandatory_for_all_levels", False)
    if dao_mandatory is True:
        ok("validation_rules.dao_layer_exam_mandatory_for_all_levels=true ✓")
    else:
        fail("validation_rules.dao_layer_exam_mandatory_for_all_levels 未设为 true")

    # [9] PIPL 合规
    print("\n[9] PIPL 合规")
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
        print("  ✅ 教练认证等级 schema 验证 PASS — 5等级认证/⑤守护递增/飞轮/七阶 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
