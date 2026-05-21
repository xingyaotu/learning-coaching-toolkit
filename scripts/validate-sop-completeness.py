#!/usr/bin/env python3
"""
道层 SOP 完整性验证脚本 v1.1
验证 coaching-sops/ 目录下的 14 个 SOP 文件完整性与道层合规性,
并交叉校验 pipeline-data/sop-skill-catalog.json 条目与 SOP 文件一致性。
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SOP_ROOT = REPO_ROOT / "coaching-sops"

# ── 期望的 SOP 文件清单 ────────────────────────────────────────

EIGHT_STEP_SOPS = {
    1: "SOP_01-穿透.md",
    2: "SOP_02-提取.md",
    3: "SOP_03-整理.md",
    4: "SOP_04-审题.md",
    5: "SOP_05-流程.md",   # ★ 绝不是 SOP_05-演示.md
    6: "SOP_06-批改.md",
    7: "SOP_07-分析.md",
    8: "SOP_08-估分.md",
}

FLYWHEEL_SOPS = {
    1: "SOP_FW1-计划飞轮.md",
    2: "SOP_FW2-预习飞轮.md",
    3: "SOP_FW3-复习飞轮.md",
    4: "SOP_FW4-听课飞轮.md",
    5: "SOP_FW5-作业飞轮.md",
    6: "SOP_FW6-考试飞轮.md",
}

# ── 道层漂移关键词(不应出现在 SOP 标题或 H1 中) ──────────────
STEP5_DRIFT_FILENAMES = {"SOP_05-演示.md", "SOP_05-demo.md", "SOP_05-demonstration.md"}
# 非法飞轮文件名(4类)
ILLEGAL_FLYWHEEL_PREFIXES = ["SOP_FW"]  # combined with illegal suffixes checked separately

FAIL = False
ERRORS: list[str] = []


def err(msg: str) -> None:
    global FAIL
    FAIL = True
    ERRORS.append(f"❌ {msg}")
    print(f"❌ {msg}", file=sys.stderr)


def ok(msg: str) -> None:
    print(f"✅ {msg}")


def validate_eight_step_sops() -> None:
    sop_dir = SOP_ROOT / "eight-step-sops"
    if not sop_dir.exists():
        err(f"eight-step-sops 目录不存在: {sop_dir}")
        return

    for step_id, filename in EIGHT_STEP_SOPS.items():
        path = sop_dir / filename
        if path.exists():
            ok(f"八步 SOP_{step_id:02d} ✓ {filename}")
        else:
            err(f"缺少八步 SOP 文件: {filename}")

    # ⑤流程守护: 确认 SOP_05 是"流程"而非"演示"
    for drift_name in STEP5_DRIFT_FILENAMES:
        if (sop_dir / drift_name).exists():
            err(f"发现漂移文件 {drift_name}，⑤必须是'流程'")

    # 确认文件数量
    actual = list(sop_dir.glob("SOP_*.md"))
    if len(actual) == 8:
        ok(f"八步 SOP 数量: {len(actual)}/8 ✓")
    else:
        err(f"八步 SOP 数量异常: 期望 8，实际 {len(actual)}")


def validate_flywheel_sops() -> None:
    sop_dir = SOP_ROOT / "flywheel-sops"
    if not sop_dir.exists():
        err(f"flywheel-sops 目录不存在: {sop_dir}")
        return

    for fw_id, filename in FLYWHEEL_SOPS.items():
        path = sop_dir / filename
        if path.exists():
            ok(f"飞轮 SOP_FW{fw_id} ✓ {filename}")
        else:
            err(f"缺少飞轮 SOP 文件: {filename}")

    # 确认文件数量 == 6
    actual = list(sop_dir.glob("SOP_FW*.md"))
    if len(actual) == 6:
        ok(f"飞轮 SOP 数量: {len(actual)}/6 ✓")
    else:
        err(f"飞轮 SOP 数量异常: 期望 6，实际 {len(actual)}")


def validate_index_json() -> None:
    import json

    index_path = SOP_ROOT / "index.json"
    if not index_path.exists():
        err(f"coaching-sops/index.json 不存在")
        return

    with open(index_path, encoding="utf-8") as f:
        index = json.load(f)

    eight_sops = index.get("eight_step_sops", [])
    flywheel_sops = index.get("flywheel_sops", [])
    total = len(eight_sops) + len(flywheel_sops)

    if total == 14:
        ok(f"index.json SOP 条目: {total}/14 ✓ (八步{len(eight_sops)} + 飞轮{len(flywheel_sops)})")
    else:
        err(f"index.json SOP 条目期望 14，实际 {total} (八步{len(eight_sops)} + 飞轮{len(flywheel_sops)})")

    # SOP_05 名称检查（⑤=流程）
    sop05 = next((s for s in eight_sops if s.get("sop_id") == "SOP_05"), None)
    if sop05:
        name = sop05.get("name_zh", "")
        if name == "流程":
            ok(f"index.json SOP_05.name_zh='流程' ✓")
        else:
            err(f"index.json SOP_05.name_zh='{name}'，期望'流程'(⑤绝非演示)")
    else:
        err("index.json eight_step_sops 中未找到 SOP_05")

    # 六飞轮数量检查
    if len(flywheel_sops) == 6:
        ok(f"index.json flywheel_sops 数量 6/6 ✓")
    else:
        err(f"index.json flywheel_sops 期望 6，实际 {len(flywheel_sops)}")


def validate_sop_count_total() -> None:
    eight = len(list((SOP_ROOT / "eight-step-sops").glob("SOP_*.md")))
    fly = len(list((SOP_ROOT / "flywheel-sops").glob("SOP_FW*.md")))
    total = eight + fly
    if total == 14:
        ok(f"SOP 总数: {total}/14 ✓")
    else:
        err(f"SOP 总数期望 14，实际 {total}")


VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_FLYWHEEL_FULL_NAMES = {
    "计划飞轮", "预习飞轮", "复习飞轮", "听课飞轮", "作业飞轮", "考试飞轮",
}
ILLEGAL_FLYWHEEL_NAMES = {"错题飞轮", "笔记飞轮", "阅读飞轮", "实践飞轮"}


def validate_sop_skill_catalog() -> None:
    import json

    catalog_path = REPO_ROOT / "pipeline-data" / "sop-skill-catalog.json"
    if not catalog_path.exists():
        err(f"pipeline-data/sop-skill-catalog.json 不存在")
        return

    with open(catalog_path, encoding="utf-8") as f:
        catalog = json.load(f)

    # ── $schema 字段 ──────────────────────────────────────────────
    if "$schema" in catalog:
        ok("sop-skill-catalog.json $schema 字段存在 ✓")
    else:
        err("sop-skill-catalog.json 缺少 $schema 字段")

    eight_entries = catalog.get("eight_step_sops", [])
    flywheel_entries = catalog.get("flywheel_sops", [])
    total = len(eight_entries) + len(flywheel_entries)

    # ── 总数 14 ───────────────────────────────────────────────────
    if total == 14:
        ok(f"sop-skill-catalog.json 条目总数 {total}/14 ✓ (八步{len(eight_entries)} + 飞轮{len(flywheel_entries)})")
    else:
        err(f"sop-skill-catalog.json 条目期望 14，实际 {total}")

    # ── 八步 SOP 条目 × 文件一致性 ───────────────────────────────
    catalog_eight_ids = set()
    for entry in eight_entries:
        sop_id = entry.get("sop_id", "?")
        catalog_eight_ids.add(sop_id)
        file_rel = entry.get("file", "")
        file_path = REPO_ROOT / file_rel
        if file_path.exists():
            ok(f"catalog → 文件存在: {file_rel} ✓")
        else:
            err(f"catalog 条目 {sop_id} 指向文件不存在: {file_rel}")

    # ── SOP_05 八步名称守护 ───────────────────────────────────────
    sop05_entries = [e for e in eight_entries if e.get("sop_id") == "SOP_05"]
    if sop05_entries:
        step_name = sop05_entries[0].get("eight_step_name", "")
        if step_name == "流程":
            ok(f"catalog SOP_05.eight_step_name='流程' ✓")
        else:
            err(f"catalog SOP_05.eight_step_name='{step_name}'，期望'流程'(⑤守护)")
        step_id = sop05_entries[0].get("eight_step_id")
        if step_id == 5:
            ok(f"catalog SOP_05.eight_step_id=5 ✓")
        else:
            err(f"catalog SOP_05.eight_step_id={step_id}，期望 5")
    else:
        err("catalog eight_step_sops 中未找到 SOP_05")

    # ── 飞轮 SOP 条目 × 文件一致性 & 名称合规 ─────────────────────
    for entry in flywheel_entries:
        sop_id = entry.get("sop_id", "?")
        file_rel = entry.get("file", "")
        file_path = REPO_ROOT / file_rel
        if file_path.exists():
            ok(f"catalog → 文件存在: {file_rel} ✓")
        else:
            err(f"catalog 条目 {sop_id} 指向文件不存在: {file_rel}")

        fw_name = entry.get("six_flywheel_name", "")
        if fw_name in VALID_FLYWHEEL_NAMES:
            ok(f"catalog {sop_id}.six_flywheel_name='{fw_name}' 合规 ✓")
        elif fw_name in ILLEGAL_FLYWHEEL_NAMES:
            err(f"catalog {sop_id}.six_flywheel_name='{fw_name}' 非法变体")
        else:
            err(f"catalog {sop_id}.six_flywheel_name='{fw_name}' 不在六飞轮枚举中")

    # ── 文件 → catalog 反向检查(文件有无对应条目) ─────────────────
    all_catalog_files = {
        (REPO_ROOT / e.get("file", "")).resolve()
        for e in eight_entries + flywheel_entries
    }
    for step_id, filename in EIGHT_STEP_SOPS.items():
        fp = (REPO_ROOT / "coaching-sops" / "eight-step-sops" / filename).resolve()
        if fp in all_catalog_files:
            ok(f"文件 → catalog 有对应条目: {filename} ✓")
        else:
            err(f"文件 {filename} 在 sop-skill-catalog.json 中无对应条目")
    for fw_id, filename in FLYWHEEL_SOPS.items():
        fp = (REPO_ROOT / "coaching-sops" / "flywheel-sops" / filename).resolve()
        if fp in all_catalog_files:
            ok(f"文件 → catalog 有对应条目: {filename} ✓")
        else:
            err(f"文件 {filename} 在 sop-skill-catalog.json 中无对应条目")


if __name__ == "__main__":
    print("=" * 60)
    print("  星耀途 SOP 完整性验证 v1.1")
    print("=" * 60)

    print("\n[1] 八步 SOP 文件验证")
    validate_eight_step_sops()

    print("\n[2] 飞轮 SOP 文件验证")
    validate_flywheel_sops()

    print("\n[3] coaching-sops/index.json 验证")
    validate_index_json()

    print("\n[4] SOP 文件总数验证")
    validate_sop_count_total()

    print("\n[5] sop-skill-catalog.json 交叉验证")
    validate_sop_skill_catalog()

    print("\n" + "=" * 60)
    if FAIL:
        print(f"❌ 验证失败，共 {len(ERRORS)} 个错误")
        for e in ERRORS:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("✅ SOP 完整性验证全部通过 (含 sop-skill-catalog.json 交叉验证)")
        sys.exit(0)
