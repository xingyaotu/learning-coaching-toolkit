#!/usr/bin/env python3
"""
道层 colleague-skill SKILL.md 验证脚本 v1.0
验证 colleague-skills/ 目录下 14 个 SKILL.md 文件的 frontmatter 合规性。
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SKILL_ROOT = REPO_ROOT / "colleague-skills"

REQUIRED_FRONTMATTER_KEYS = {"name", "description", "version", "allowed-tools", "portal", "quadruple_context"}
VALID_PORTALS = {"xyt-coach", "xyt-student", "xyt-parent", "xyt-hq"}

EIGHT_STEP_FILES = {f"sop-0{i}.skill.md" for i in range(1, 9)}
FLYWHEEL_FILES = {f"sop-fw{i}.skill.md" for i in range(1, 7)}

FAIL = False
ERRORS: list[str] = []


def err(msg: str) -> None:
    global FAIL
    FAIL = True
    ERRORS.append(f"❌ {msg}")
    print(f"  ❌ {msg}", file=sys.stderr)


def ok(msg: str) -> None:
    print(f"  ✅ {msg}")


def parse_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        return None
    import yaml
    try:
        return yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError:
        return None


def validate_skill_file(path: Path, expected_filename: str) -> None:
    if not path.exists():
        err(f"缺少文件: {expected_filename}")
        return

    fm = parse_frontmatter(path)
    if fm is None:
        err(f"{path.name}: frontmatter 解析失败")
        return

    # 必填字段
    missing = REQUIRED_FRONTMATTER_KEYS - set(fm.keys())
    if missing:
        err(f"{path.name}: frontmatter 缺少字段 {missing}")
    else:
        ok(f"{path.name}: frontmatter 字段完整 ✓")

    # portal 合规
    portal = fm.get("portal", "")
    if portal not in VALID_PORTALS:
        err(f"{path.name}: portal='{portal}' 不在合法值 {VALID_PORTALS}")
    else:
        ok(f"{path.name}: portal={portal} ✓")

    # quadruple_context
    qc = fm.get("quadruple_context", {})
    if not isinstance(qc, dict):
        err(f"{path.name}: quadruple_context 格式错误")

    return fm


def validate_sop05_guard(path: Path) -> None:
    """SOP_05 ⑤守护: eight_step_id=5, eight_step_name=流程"""
    fm = parse_frontmatter(path)
    if fm is None:
        err("sop-05.skill.md: frontmatter 无法读取")
        return
    qc = fm.get("quadruple_context", {})
    step_id = qc.get("eight_step_id")
    step_name = qc.get("eight_step_name")
    if step_id == 5:
        ok(f"sop-05 eight_step_id=5 ✓")
    else:
        err(f"sop-05 eight_step_id={step_id}，期望 5")
    if step_name == "流程":
        ok(f"sop-05 eight_step_name='流程' ✓ ⑤守护通过")
    else:
        err(f"sop-05 eight_step_name='{step_name}'，期望'流程'(⑤守护)")


def validate_flywheel_names(sop_dir: Path) -> None:
    """六飞轮名称守护"""
    valid_names = {"计划", "预习", "复习", "听课", "作业", "考试"}
    illegal = {"错题", "笔记", "阅读", "实践"}
    seen_names: set[str] = set()
    for f in sorted(sop_dir.glob("sop-fw*.skill.md")):
        fm = parse_frontmatter(f)
        if fm is None:
            continue
        qc = fm.get("quadruple_context", {})
        fw_name = qc.get("six_flywheel_name", "")
        if fw_name in illegal:
            err(f"{f.name}: six_flywheel_name='{fw_name}' 非法变体")
        elif fw_name in valid_names:
            ok(f"{f.name}: six_flywheel_name='{fw_name}' 合规 ✓")
            seen_names.add(fw_name)
        else:
            err(f"{f.name}: six_flywheel_name='{fw_name}' 不在六飞轮枚举")
    if len(seen_names) == 6:
        ok(f"六飞轮名称全枚举覆盖 6/6 ✓")
    else:
        missing = valid_names - seen_names
        err(f"六飞轮未覆盖: {missing}")


if __name__ == "__main__":
    print("=" * 55)
    print("  colleague-skill SKILL.md 验证 v1.0")
    print("=" * 55)

    # [1] 目录存在性
    print("\n[1] colleague-skills/ 目录结构")
    for subdir in ["eight-step-sops", "flywheel-sops"]:
        p = SKILL_ROOT / subdir
        if p.exists():
            ok(f"目录存在: {subdir}/")
        else:
            err(f"目录缺失: {subdir}/")

    # [2] 八步 SOP SKILL.md 文件验证
    print("\n[2] 八步 SOP SKILL.md (8 个)")
    eight_dir = SKILL_ROOT / "eight-step-sops"
    for filename in sorted(EIGHT_STEP_FILES):
        validate_skill_file(eight_dir / filename, filename)

    # [3] SOP_05 ⑤守护
    print("\n[3] SOP_05 ⑤守护验证")
    validate_sop05_guard(eight_dir / "sop-05.skill.md")

    # [4] 飞轮 SOP SKILL.md 文件验证
    print("\n[4] 飞轮 SOP SKILL.md (6 个)")
    flywheel_dir = SKILL_ROOT / "flywheel-sops"
    for filename in sorted(FLYWHEEL_FILES):
        validate_skill_file(flywheel_dir / filename, filename)

    # [5] 六飞轮名称守护
    print("\n[5] 六飞轮名称守护")
    validate_flywheel_names(flywheel_dir)

    # [6] 总数校验
    print("\n[6] SKILL.md 总数")
    actual_eight = len(list(eight_dir.glob("sop-*.skill.md"))) if eight_dir.exists() else 0
    actual_fw = len(list(flywheel_dir.glob("sop-fw*.skill.md"))) if flywheel_dir.exists() else 0
    total = actual_eight + actual_fw
    if total == 14:
        ok(f"SKILL.md 总数 {total}/14 ✓ (八步{actual_eight} + 飞轮{actual_fw})")
    else:
        err(f"SKILL.md 总数期望 14，实际 {total}")

    print("\n" + "=" * 55)
    if FAIL:
        print(f"❌ 验证失败，共 {len(ERRORS)} 个错误")
        for e in ERRORS:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("✅ colleague-skill SKILL.md 验证全部通过 (14/14)")
        sys.exit(0)
