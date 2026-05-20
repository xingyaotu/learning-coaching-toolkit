#!/usr/bin/env python3
"""
道层 SOP 完整性验证脚本 v1.0
验证 coaching-sops/ 目录下的 14 个 SOP 文件完整性与道层合规性。
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


if __name__ == "__main__":
    print("=" * 50)
    print("  星耀途 SOP 完整性验证 v1.0")
    print("=" * 50)

    validate_eight_step_sops()
    validate_flywheel_sops()
    validate_index_json()
    validate_sop_count_total()

    print("=" * 50)
    if FAIL:
        print(f"❌ 验证失败，共 {len(ERRORS)} 个错误")
        sys.exit(1)
    else:
        print("✅ SOP 完整性验证全部通过")
        sys.exit(0)
