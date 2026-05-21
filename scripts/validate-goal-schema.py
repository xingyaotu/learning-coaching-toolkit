#!/usr/bin/env python3
"""
道层教练目标 schema 验证脚本 v1.0
验证 pipeline-data/coaching-goal-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. schema_definitions 类型完整 (coaching_goal + goal_revision_record)
  3. goal_templates: 6个模板覆盖 1→2 至 6→7 所有相邻阶位跃迁
  4. goal_templates: target_stage > baseline_stage
  5. goal_templates: recommended_sops 的 sop_ref 在 sop-skill-catalog 中存在
  6. goal_templates: priority 值合规
  7. ⑤守护: 所有引用 sop-05 的模板包含 _sop05_note 或 validation_rules 含流程约束
  8. validation_rules.six_flywheel_valid_names 枚举 6个
  9. PIPL 合规声明
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
GOAL_PATH = REPO_ROOT / "pipeline-data" / "coaching-goal-schema.json"
CATALOG_PATH = REPO_ROOT / "pipeline-data" / "sop-skill-catalog.json"

REQUIRED_SCHEMA_TYPES = {"coaching_goal", "goal_revision_record"}
VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_PRIORITIES = {"必做", "强化", "巩固", "精进"}
EXPECTED_TRANSITIONS = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]

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
    print("  教练目标 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not GOAL_PATH.exists():
        fail(f"找不到文件: {GOAL_PATH}")
        sys.exit(1)
    if not CATALOG_PATH.exists():
        fail(f"找不到 catalog: {CATALOG_PATH}")
        sys.exit(1)
    goal_schema = json.loads(GOAL_PATH.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    ok("coaching-goal-schema.json + catalog 加载成功")

    # Build valid SOP refs from catalog
    valid_sop_refs = set()
    for s in catalog.get("eight_step_sops", []):
        valid_sop_refs.add(f"sop-0{s['eight_step_id']}")
    for s in catalog.get("flywheel_sops", []):
        valid_sop_refs.add(f"sop-fw{s['six_flywheel_id']}")

    # [2] schema_definitions 完整性
    print("\n[2] schema_definitions 类型完整")
    defs = set(goal_schema.get("schema_definitions", {}).keys())
    missing = REQUIRED_SCHEMA_TYPES - defs
    if missing:
        fail(f"缺少 schema 类型: {missing}")
    else:
        ok(f"schema_definitions 类型完整: {sorted(defs)} ✓")

    # [3-6] goal_templates
    print("\n[3-6] goal_templates 阶位跃迁 + SOP 合规")
    templates = goal_schema.get("goal_templates", [])
    found_transitions = set()
    for t in templates:
        tid = t.get("template_id", "?")
        bs = t.get("baseline_stage")
        ts = t.get("target_stage")
        found_transitions.add((bs, ts))

        # target > baseline
        if ts is not None and bs is not None and ts > bs:
            ok(f"{tid}: target_stage={ts} > baseline_stage={bs} ✓")
        else:
            fail(f"{tid}: target_stage={ts} ≤ baseline_stage={bs}")

        # recommended_sops
        for sop in t.get("recommended_sops", []):
            ref = sop.get("sop_ref", "?")
            priority = sop.get("priority", "?")
            if ref in valid_sop_refs:
                ok(f"{tid}/{ref}: sop_ref 存在 ✓")
            else:
                fail(f"{tid}/{ref}: sop_ref 不在 catalog 中 (valid={sorted(valid_sop_refs)})")
            if priority in VALID_PRIORITIES:
                ok(f"{tid}/{ref}: priority='{priority}' ✓")
            else:
                fail(f"{tid}/{ref}: priority='{priority}' 不合规")

    # [3] transition coverage
    missing_trans = set(EXPECTED_TRANSITIONS) - found_transitions
    if missing_trans:
        fail(f"缺少阶位跃迁模板: {missing_trans}")
    else:
        ok(f"6个相邻阶位跃迁模板全覆盖 (1→2 至 6→7) ✓")

    # [7] ⑤守护 — validation_rules
    print("\n[7] ⑤守护验证")
    vr = goal_schema.get("validation_rules", {})
    eight_constraint = vr.get("eight_step_name_constraints", {})
    step5_name = eight_constraint.get("step_id_5_name", "")
    if step5_name == "流程":
        ok("validation_rules step_id_5_name='流程' ⑤守护 ✓")
    else:
        fail(f"validation_rules step_id_5_name='{step5_name}' ≠ '流程'")

    # Check sop-05 templates have _sop05_note
    for t in templates:
        has_sop05 = any(s.get("sop_ref") == "sop-05" for s in t.get("recommended_sops", []))
        if has_sop05 and "_sop05_note" in t:
            ok(f"{t['template_id']}: 引用 sop-05 且含 _sop05_note 守护字段 ✓")

    # [8] 六飞轮枚举
    print("\n[8] validation_rules.six_flywheel_valid_names 枚举")
    fw_names = set(vr.get("six_flywheel_valid_names", []))
    missing_fw = VALID_FLYWHEEL_NAMES - fw_names
    if missing_fw:
        fail(f"six_flywheel_valid_names 缺少: {missing_fw}")
    elif len(fw_names) == 6:
        ok(f"六飞轮 valid_names 6个全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names 数量 {len(fw_names)} ≠ 6")

    # [9] PIPL 合规声明
    print("\n[9] PIPL 合规声明")
    privacy = goal_schema.get("_meta", {}).get("privacy_note", "")
    if "PIPL" in privacy:
        ok(f"PIPL 合规声明存在 ✓")
    else:
        fail("_meta.privacy_note 缺少 PIPL 合规声明")

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
        print("  ✅ 教练目标 schema 验证 PASS — 全部道层规范合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
