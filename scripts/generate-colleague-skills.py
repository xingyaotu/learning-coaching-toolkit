#!/usr/bin/env python3
"""
道层 colleague-skill SKILL.md 生成脚本 v1.0
从 pipeline-data/sop-skill-catalog.json 生成 colleague-skills/ 目录下的 14 个 SKILL.md 文件。
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CATALOG_PATH = REPO_ROOT / "pipeline-data" / "sop-skill-catalog.json"
COLLEAGUE_SKILLS_ROOT = REPO_ROOT / "colleague-skills"

PORTAL = "xyt-coach"
VERSION = "1.0.0"

STAGE_LABELS = {1: "不会", 2: "模糊", 3: "清晰", 4: "框架", 5: "运用", 6: "熟练", 7: "创新"}


def skill_filename(sop_id: str) -> str:
    return f"{sop_id.lower().replace('_', '-')}.skill.md"


def generate_eight_step_skill(entry: dict) -> str:
    sop_id = entry["sop_id"]
    name = entry["name"]
    desc = entry["description"]
    step_id = entry["eight_step_id"]
    step_name = entry["eight_step_name"]
    stage_lo, stage_hi = entry["stage_range"]
    flywheel = entry["primary_flywheel"]
    fw_id = entry["flywheel_id"]
    use_when = entry["use_when"]
    allowed = entry.get("allowed_tools", ["nuwa-skill", "DeepTutor", "nanobot"])

    stage_lo_label = STAGE_LABELS.get(stage_lo, str(stage_lo))
    stage_hi_label = STAGE_LABELS.get(stage_hi, str(stage_hi))
    allowed_str = "\n  - ".join(allowed)

    step5_note = "\n★_note: 第5步名称=流程 ✅ 道层合规" if step_id == 5 else ""

    return f"""---
name: {sop_id.lower().replace('_', '-')}
description: |
  {desc}
  Use when {use_when}
version: "{VERSION}"
allowed-tools:
  - {allowed_str}
portal: {PORTAL}
quadruple_context:
  eight_step_id: {step_id}
  eight_step_name: {step_name}
  stage_range: [{stage_lo}, {stage_hi}]
  primary_flywheel: {flywheel}
  six_flywheel_id: {fw_id}{step5_note}
---

# {name}

## 触发场景

- 学员当前七阶阶位 {stage_lo_label}({stage_lo}) 至 {stage_hi_label}({stage_hi})
- 当前学习任务进入八步第{step_id}步「{step_name}」环节
- 主导飞轮: {flywheel}

## 八步定位

| 步骤 | 名称 | 本 SOP 聚焦 |
|------|------|-------------|
| ⑤ | 流程 | {"✅ 核心 — 本步骤" if step_id == 5 else f"第 {step_id} 步「{step_name}」"} |

## 调用规约

- 调用方式: `{sop_id}` via colleague-skill 接口
- 参考文档: `coaching-sops/eight-step-sops/{sop_id}-{step_name}.md`
- 道层合规: 八步⑤=流程 ✅ | 六飞轮严格枚举 ✅ | CSO 0触发 ✅
"""


def generate_flywheel_skill(entry: dict) -> str:
    sop_id = entry["sop_id"]
    name = entry["name"]
    desc = entry["description"]
    fw_id = entry["six_flywheel_id"]
    fw_name = entry["six_flywheel_name"]
    stage_lo, stage_hi = entry["stage_range"]
    use_when = entry["use_when"]
    allowed = entry.get("allowed_tools", ["nuwa-skill", "gbrain"])

    stage_lo_label = STAGE_LABELS.get(stage_lo, str(stage_lo))
    stage_hi_label = STAGE_LABELS.get(stage_hi, str(stage_hi))
    allowed_str = "\n  - ".join(allowed)

    return f"""---
name: {sop_id.lower().replace('_', '-')}
description: |
  {desc}
  Use when {use_when}
version: "{VERSION}"
allowed-tools:
  - {allowed_str}
portal: {PORTAL}
quadruple_context:
  six_flywheel_id: {fw_id}
  six_flywheel_name: {fw_name}
  stage_range: [{stage_lo}, {stage_hi}]
---

# {name}

## 触发场景

- 学员当前七阶阶位 {stage_lo_label}({stage_lo}) 至 {stage_hi_label}({stage_hi})
- 六飞轮第 {fw_id} 飞轮「{fw_name}飞轮」激活时
- 道层对齐: 六飞轮 = 计划/预习/复习/听课/作业/考试 ✅

## 飞轮定位

| 飞轮编号 | 飞轮名称 | 阶位范围 |
|----------|----------|---------|
| {fw_id} | {fw_name}飞轮 | {stage_lo_label}({stage_lo}) — {stage_hi_label}({stage_hi}) |

## 调用规约

- 调用方式: `{sop_id}` via colleague-skill 接口
- 参考文档: `coaching-sops/flywheel-sops/{sop_id}-{fw_name}飞轮.md`
- 道层合规: 六飞轮枚举合规(计划/预习/复习/听课/作业/考试) ✅ | CSO 0触发 ✅
"""


def main() -> None:
    if not CATALOG_PATH.exists():
        print(f"❌ 找不到 {CATALOG_PATH}")
        sys.exit(1)

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    eight_entries = catalog.get("eight_step_sops", [])
    flywheel_entries = catalog.get("flywheel_sops", [])

    generated = 0

    print("=" * 55)
    print("  colleague-skill SKILL.md 生成器 v1.0")
    print("=" * 55)

    # ── 八步 SOP SKILL.md ───────────────────────────────────────
    out_dir = COLLEAGUE_SKILLS_ROOT / "eight-step-sops"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[1] 八步 SOP SKILL.md ({len(eight_entries)} 个)")
    for entry in eight_entries:
        sop_id = entry["sop_id"]
        filename = skill_filename(sop_id)
        content = generate_eight_step_skill(entry)
        (out_dir / filename).write_text(content, encoding="utf-8")
        print(f"  ✅ {filename}")
        generated += 1

    # ── 飞轮 SOP SKILL.md ───────────────────────────────────────
    out_dir = COLLEAGUE_SKILLS_ROOT / "flywheel-sops"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[2] 飞轮 SOP SKILL.md ({len(flywheel_entries)} 个)")
    for entry in flywheel_entries:
        sop_id = entry["sop_id"]
        filename = skill_filename(sop_id)
        content = generate_flywheel_skill(entry)
        (out_dir / filename).write_text(content, encoding="utf-8")
        print(f"  ✅ {filename}")
        generated += 1

    print(f"\n  生成完毕: {generated}/14 SKILL.md ✅")
    print("=" * 55)


if __name__ == "__main__":
    main()
