#!/usr/bin/env python3
"""
道层教练会话模板验证脚本 v1.0
验证 pipeline-data/coaching-session-templates.json 的合规性。

验证项:
  1. JSON 文件加载
  2. 八步模板数量 == 8; step_id 1-8 全覆盖; step_name 枚举正确
  3. SOP-05 ⑤守护: eight_step_name == '流程'
  4. 飞轮模板数量 == 6; flywheel_id 1-6; flywheel_name 枚举正确
  5. 所有 target_stages ∈ {1-7}
  6. 每个模板 session_structure 时长之和 <= 60 分钟
  7. skill_interface 路径存在性检查
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TEMPLATE_PATH = REPO_ROOT / "pipeline-data" / "coaching-session-templates.json"

VALID_STAGE_IDS = set(range(1, 8))
EIGHT_STEP_NAMES = {
    1: "穿透", 2: "提取", 3: "整理", 4: "审题",
    5: "流程", 6: "批改", 7: "分析", 8: "估分",
}
FLYWHEEL_NAMES = {
    1: "计划", 2: "预习", 3: "复习",
    4: "听课", 5: "作业", 6: "考试",
}
MAX_SESSION_MINUTES = 60

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


def validate_template_common(tpl: dict, ctx: str) -> None:
    """Validate target_stages, session_structure duration, skill_interface."""
    # target_stages
    stages = tpl.get("target_stages", [])
    if not stages:
        fail(f"{ctx}: target_stages 为空")
    else:
        invalid = set(stages) - VALID_STAGE_IDS
        if invalid:
            fail(f"{ctx}: target_stages 含非法值 {invalid}")
        else:
            ok(f"{ctx}: target_stages={stages} 合规 ✓")

    # session_structure total duration
    structure = tpl.get("session_structure", [])
    total_min = sum(p.get("duration_min", 0) for p in structure)
    if total_min > MAX_SESSION_MINUTES:
        fail(f"{ctx}: session_structure 总时长 {total_min}min > {MAX_SESSION_MINUTES}min")
    else:
        ok(f"{ctx}: session_structure 时长 {total_min}min ≤ {MAX_SESSION_MINUTES}min ✓")

    # skill_interface path existence
    si = tpl.get("skill_interface", "")
    si_path = REPO_ROOT / si
    if si_path.exists():
        ok(f"{ctx}: skill_interface 路径存在 ✓")
    else:
        fail(f"{ctx}: skill_interface 路径不存在: {si}")


def main() -> None:
    print("=" * 62)
    print("  教练会话模板验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not TEMPLATE_PATH.exists():
        fail(f"找不到模板文件: {TEMPLATE_PATH}")
        sys.exit(1)
    templates = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    ok("coaching-session-templates.json 加载成功")

    eight_templates = templates.get("eight_step_session_templates", [])
    fw_templates = templates.get("flywheel_session_templates", [])

    # [2] 八步模板数量 + 枚举
    print("\n[2] 八步模板 (8个, step_id 1-8)")
    if len(eight_templates) == 8:
        ok(f"八步模板数量 = 8 ✓")
    else:
        fail(f"八步模板数量 = {len(eight_templates)}，期望 8")

    found_step_ids = set()
    for t in eight_templates:
        sid = t.get("eight_step_id")
        sname = t.get("eight_step_name", "")
        expected = EIGHT_STEP_NAMES.get(sid, "?")
        if sname == expected:
            ok(f"步 {sid} '{sname}' 枚举正确 ✓")
        else:
            fail(f"步 {sid} name='{sname}' 期望 '{expected}'")
        found_step_ids.add(sid)
        validate_template_common(t, f"sop-0{sid}")

    missing_steps = set(range(1, 9)) - found_step_ids
    if missing_steps:
        fail(f"缺少八步模板: step_id {missing_steps}")
    else:
        ok("八步 1-8 全量覆盖 ✓")

    # [3] ⑤守护
    print("\n[3] SOP-05 ⑤守护验证")
    sop05 = next((t for t in eight_templates if t.get("eight_step_id") == 5), None)
    if sop05 is None:
        fail("SOP-05 模板缺失")
    elif sop05.get("eight_step_name") == "流程":
        ok(f"SOP-05 eight_step_name='流程' ⑤守护通过 ✓")
    else:
        fail(f"SOP-05 eight_step_name='{sop05.get('eight_step_name')}' ≠ '流程' ⑤守护失败")

    # [4] 飞轮模板数量 + 枚举
    print("\n[4] 飞轮模板 (6个, flywheel_id 1-6)")
    if len(fw_templates) == 6:
        ok(f"飞轮模板数量 = 6 ✓")
    else:
        fail(f"飞轮模板数量 = {len(fw_templates)}，期望 6")

    found_fw_ids = set()
    for t in fw_templates:
        fid = t.get("six_flywheel_id")
        fname = t.get("six_flywheel_name", "")
        expected = FLYWHEEL_NAMES.get(fid, "?")
        if fname == expected:
            ok(f"飞轮 {fid} '{fname}' 枚举正确 ✓")
        else:
            fail(f"飞轮 {fid} name='{fname}' 期望 '{expected}'")
        found_fw_ids.add(fid)
        validate_template_common(t, f"sop-fw{fid}")

    missing_fw = set(range(1, 7)) - found_fw_ids
    if missing_fw:
        fail(f"缺少飞轮模板: flywheel_id {missing_fw}")
    else:
        ok("六飞轮 1-6 全量覆盖 ✓")

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
        print("  ✅ 教练会话模板验证 PASS — 14个模板全部合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
