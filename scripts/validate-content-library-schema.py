#!/usr/bin/env python3
"""
道层教练内容库 schema 验证脚本 v1.0
验证 pipeline-data/coaching-content-library-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. content_item_schema: 6个必填字段
  3. target_flywheel enum 六飞轮 + _dao_guard
  4. target_stage_range properties 含七阶 enum + _dao_guard 含'七阶'
  5. mece_dimension_tags items enum MECE + _dao_guard
  6. sop05_alignment _dao_guard 含'流程' ⑤守护
  7. content_assignment_schema: student_stage_at_assignment enum 七阶 + _dao_guard
  8. flywheel_targeted enum 六飞轮 + _dao_guard
  9. sop05_practiced _dao_guard 含'流程' ⑤守护
  10. content_library_stats: items_by_flywheel 六飞轮 + _dao_guard
  11. items_by_stage_range 七阶 + _dao_guard
  12. sop05_practice_rate _dao_guard 含'流程' ⑤守护
  13. validation_rules: sop05_guard/七阶/MECE/六飞轮/pipl
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CONTENT_PATH = REPO_ROOT / "pipeline-data" / "coaching-content-library-schema.json"

VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}
MECE_DIMENSIONS = {"M", "E_exec", "C", "E_env"}
REQUIRED_CONTENT_FIELDS = {
    "content_id", "content_title", "content_type",
    "target_flywheel", "difficulty_level", "is_active"
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
    print("  教练内容库 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not CONTENT_PATH.exists():
        fail(f"找不到文件: {CONTENT_PATH}")
        sys.exit(1)
    data = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    ok("coaching-content-library-schema.json 加载成功")

    ci_fields = data.get("content_item_schema", {}).get("fields", {})
    ca_fields = data.get("content_assignment_schema", {}).get("fields", {})
    cls_fields = data.get("content_library_stats", {}).get("fields", {})
    vr = data.get("validation_rules", {})

    # [2] content_item_schema 必填字段
    print("\n[2] content_item_schema 6个必填字段")
    for fname in REQUIRED_CONTENT_FIELDS:
        if fname in ci_fields:
            ok(f"content_item_schema.fields.{fname} 存在 ✓")
        else:
            fail(f"content_item_schema.fields.{fname} 缺失")

    # [3] target_flywheel enum 六飞轮 + _dao_guard
    print("\n[3] target_flywheel enum 六飞轮 + _dao_guard")
    tf_field = ci_fields.get("target_flywheel", {})
    tf_enum = set(tf_field.get("enum", []))
    if tf_enum == VALID_FLYWHEEL_NAMES:
        ok("target_flywheel enum 六飞轮全覆盖 ✓")
    else:
        fail(f"target_flywheel enum {tf_enum} ≠ {VALID_FLYWHEEL_NAMES}")
    tf_guard = tf_field.get("_dao_guard", "")
    if "六飞轮" in tf_guard:
        ok("target_flywheel._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"target_flywheel._dao_guard='{tf_guard}' 未含'六飞轮'")

    # [4] target_stage_range _dao_guard 含'七阶'
    print("\n[4] target_stage_range min/max 七阶 enum + _dao_guard")
    tsr_field = ci_fields.get("target_stage_range", {})
    tsr_props = tsr_field.get("properties", {})
    for key in ["min_stage", "max_stage"]:
        tsr_enum = set(tsr_props.get(key, {}).get("enum", []))
        if tsr_enum == VALID_STAGE_NAMES:
            ok(f"target_stage_range.{key} enum 七阶全覆盖 ✓")
        else:
            fail(f"target_stage_range.{key} enum {tsr_enum} ≠ {VALID_STAGE_NAMES}")
    tsr_guard = tsr_field.get("_dao_guard", "")
    if "七阶" in tsr_guard:
        ok("target_stage_range._dao_guard 含'七阶' ✓")
    else:
        fail(f"target_stage_range._dao_guard='{tsr_guard}' 未含'七阶'")

    # [5] mece_dimension_tags items enum MECE + _dao_guard
    print("\n[5] mece_dimension_tags items enum MECE + _dao_guard")
    mdt_field = ci_fields.get("mece_dimension_tags", {})
    mdt_items_enum = set(mdt_field.get("items", {}).get("enum", []))
    if mdt_items_enum == MECE_DIMENSIONS:
        ok("mece_dimension_tags items enum MECE 四维度 ✓")
    else:
        fail(f"mece_dimension_tags items enum {mdt_items_enum} ≠ {MECE_DIMENSIONS}")
    mdt_guard = mdt_field.get("_dao_guard", "")
    if "MECE" in mdt_guard:
        ok("mece_dimension_tags._dao_guard 含'MECE' ✓")
    else:
        fail(f"mece_dimension_tags._dao_guard='{mdt_guard}' 未含'MECE'")

    # [6] sop05_alignment ⑤守护
    print("\n[6] sop05_alignment ⑤守护 含'流程'")
    sa_guard = ci_fields.get("sop05_alignment", {}).get("_dao_guard", "")
    if "流程" in sa_guard:
        ok("sop05_alignment._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_alignment._dao_guard='{sa_guard}' 未含'流程'")

    # [7] content_assignment: student_stage_at_assignment enum 七阶 + _dao_guard
    print("\n[7] content_assignment student_stage_at_assignment enum 七阶 + _dao_guard")
    ssaa_field = ca_fields.get("student_stage_at_assignment", {})
    ssaa_enum = set(ssaa_field.get("enum", []))
    if ssaa_enum == VALID_STAGE_NAMES:
        ok("student_stage_at_assignment enum 七阶全覆盖 ✓")
    else:
        fail(f"student_stage_at_assignment enum {ssaa_enum} ≠ {VALID_STAGE_NAMES}")
    ssaa_guard = ssaa_field.get("_dao_guard", "")
    if "七阶" in ssaa_guard:
        ok("student_stage_at_assignment._dao_guard 含'七阶' ✓")
    else:
        fail(f"student_stage_at_assignment._dao_guard='{ssaa_guard}' 未含'七阶'")

    # [8] flywheel_targeted enum 六飞轮 + _dao_guard
    print("\n[8] content_assignment flywheel_targeted enum 六飞轮 + _dao_guard")
    fwt_field = ca_fields.get("flywheel_targeted", {})
    fwt_enum = set(fwt_field.get("enum", []))
    if fwt_enum == VALID_FLYWHEEL_NAMES:
        ok("flywheel_targeted enum 六飞轮全覆盖 ✓")
    else:
        fail(f"flywheel_targeted enum {fwt_enum} ≠ {VALID_FLYWHEEL_NAMES}")
    fwt_guard = fwt_field.get("_dao_guard", "")
    if "六飞轮" in fwt_guard:
        ok("flywheel_targeted._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"flywheel_targeted._dao_guard='{fwt_guard}' 未含'六飞轮'")

    # [9] sop05_practiced ⑤守护
    print("\n[9] content_assignment sop05_practiced ⑤守护 含'流程'")
    sop_prac_guard = ca_fields.get("sop05_practiced", {}).get("_dao_guard", "")
    if "流程" in sop_prac_guard:
        ok("sop05_practiced._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_practiced._dao_guard='{sop_prac_guard}' 未含'流程'")

    # [10] content_library_stats: items_by_flywheel 六飞轮 + _dao_guard
    print("\n[10] content_library_stats items_by_flywheel 六飞轮 + _dao_guard")
    ibf_field = cls_fields.get("items_by_flywheel", {})
    ibf_props = set(ibf_field.get("properties", {}).keys())
    if ibf_props == VALID_FLYWHEEL_NAMES:
        ok("items_by_flywheel 六飞轮全覆盖 ✓")
    else:
        fail(f"items_by_flywheel {ibf_props} ≠ {VALID_FLYWHEEL_NAMES}")
    ibf_guard = ibf_field.get("_dao_guard", "")
    if "六飞轮" in ibf_guard:
        ok("items_by_flywheel._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"items_by_flywheel._dao_guard='{ibf_guard}' 未含'六飞轮'")

    # [11] items_by_stage_range 七阶 + _dao_guard
    print("\n[11] content_library_stats items_by_stage_range 七阶 + _dao_guard")
    ibsr_field = cls_fields.get("items_by_stage_range", {})
    ibsr_props = set(ibsr_field.get("properties", {}).keys())
    if ibsr_props == VALID_STAGE_NAMES:
        ok("items_by_stage_range 七阶全覆盖 ✓")
    else:
        fail(f"items_by_stage_range {ibsr_props} ≠ {VALID_STAGE_NAMES}")
    ibsr_guard = ibsr_field.get("_dao_guard", "")
    if "七阶" in ibsr_guard:
        ok("items_by_stage_range._dao_guard 含'七阶' ✓")
    else:
        fail(f"items_by_stage_range._dao_guard='{ibsr_guard}' 未含'七阶'")

    # [12] sop05_practice_rate ⑤守护
    print("\n[12] content_library_stats sop05_practice_rate ⑤守护 含'流程'")
    spr_guard = cls_fields.get("sop05_practice_rate", {}).get("_dao_guard", "")
    if "流程" in spr_guard:
        ok("sop05_practice_rate._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_practice_rate._dao_guard='{spr_guard}' 未含'流程'")

    # [13] validation_rules
    print("\n[13] validation_rules 合规")
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
        print("  ✅ 教练内容库 schema 验证 PASS — 内容字段/⑤守护/七阶/MECE/六飞轮/PIPL 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
