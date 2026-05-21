#!/usr/bin/env python3
"""
道层教练有效性指标验证脚本 v1.0
验证 pipeline-data/coaching-effectiveness-metrics.json 的合规性。

验证项:
  1. JSON 文件加载
  2. sop_effectiveness_kpis: 8个八步 SOP 全覆盖 (step_id 1-8)
  3. flywheel_effectiveness_kpis: 6个飞轮全覆盖 (flywheel_id 1-6)
  4. ⑤守护: sop-05 eight_step_name == '流程' + _dao_guard 字段存在
  5. 八步名称枚举合规
  6. 六飞轮名称枚举合规
  7. KPI target 值类型检查 (numeric)
  8. aggregated_kpis 公式系数之和 == 1.0
  9. validation_rules.six_flywheel_valid_names 枚举 6个
"""

import json
import sys
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
METRICS_PATH = REPO_ROOT / "pipeline-data" / "coaching-effectiveness-metrics.json"

EIGHT_STEP_NAMES = {
    1: "穿透", 2: "提取", 3: "整理", 4: "审题",
    5: "流程", 6: "批改", 7: "分析", 8: "估分",
}
FLYWHEEL_NAMES = {
    1: "计划", 2: "预习", 3: "复习",
    4: "听课", 5: "作业", 6: "考试",
}
VALID_FLYWHEEL_NAMES = set(FLYWHEEL_NAMES.values())

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
    print("  教练有效性指标验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not METRICS_PATH.exists():
        fail(f"找不到文件: {METRICS_PATH}")
        sys.exit(1)
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    ok("coaching-effectiveness-metrics.json 加载成功")

    eight_kpis = metrics.get("sop_effectiveness_kpis", [])
    fw_kpis = metrics.get("flywheel_effectiveness_kpis", [])

    # [2] 八步 SOP KPI 全覆盖
    print("\n[2] sop_effectiveness_kpis 八步全覆盖 (step_id 1-8)")
    found_step_ids = set()
    for s in eight_kpis:
        step_id = s.get("eight_step_id")
        step_name = s.get("eight_step_name", "")
        expected = EIGHT_STEP_NAMES.get(step_id, "?")
        found_step_ids.add(step_id)
        if step_name == expected:
            ok(f"步 {step_id} '{step_name}' ✓")
        else:
            fail(f"步 {step_id} name='{step_name}' 期望 '{expected}'")
        # validate KPI targets
        for kpi in s.get("kpis", []):
            t = kpi.get("target")
            if t is None or not isinstance(t, (int, float)):
                fail(f"步{step_id}/{kpi.get('kpi_id','?')}: target 非数值")
            else:
                ok(f"步{step_id}/{kpi.get('kpi_id','?')}: target={t} 合规 ✓")

    missing_steps = set(range(1, 9)) - found_step_ids
    if missing_steps:
        fail(f"缺少八步 KPI: {missing_steps}")
    else:
        ok("八步 1-8 KPI 全覆盖 ✓")

    # [3] 飞轮 KPI 全覆盖
    print("\n[3] flywheel_effectiveness_kpis 六飞轮全覆盖")
    found_fw_ids = set()
    for fw in fw_kpis:
        fid = fw.get("six_flywheel_id")
        fname = fw.get("six_flywheel_name", "")
        expected = FLYWHEEL_NAMES.get(fid, "?")
        found_fw_ids.add(fid)
        if fname == expected:
            ok(f"飞轮 {fid} '{fname}' ✓")
        else:
            fail(f"飞轮 {fid} name='{fname}' 期望 '{expected}'")
        for kpi in fw.get("kpis", []):
            t = kpi.get("target")
            if t is None or not isinstance(t, (int, float)):
                fail(f"飞轮{fid}/{kpi.get('kpi_id','?')}: target 非数值")

    missing_fw = set(range(1, 7)) - found_fw_ids
    if missing_fw:
        fail(f"缺少飞轮 KPI: {missing_fw}")
    else:
        ok("六飞轮 1-6 KPI 全覆盖 ✓")

    # [4] ⑤守护
    print("\n[4] ⑤守护验证")
    sop05 = next((s for s in eight_kpis if s.get("eight_step_id") == 5), None)
    if sop05 is None:
        fail("sop-05 KPI 缺失")
    else:
        if sop05.get("eight_step_name") == "流程":
            ok("sop-05 eight_step_name='流程' ✓")
        else:
            fail(f"sop-05 eight_step_name='{sop05.get('eight_step_name')}' ≠ '流程'")
        if "_dao_guard" in sop05:
            ok("sop-05 _dao_guard 字段存在 ✓")
        else:
            fail("sop-05 缺少 _dao_guard 守护字段")

    # [5] validation_rules ⑤守护
    vr = metrics.get("validation_rules", {})
    step5_name = vr.get("eight_step_name_constraints", {}).get("step_id_5_name", "")
    if step5_name == "流程":
        ok("validation_rules step_id_5_name='流程' ⑤联动守护 ✓")
    else:
        fail(f"validation_rules step_id_5_name='{step5_name}' ≠ '流程'")

    # [6] 六飞轮枚举
    print("\n[5] validation_rules.six_flywheel_valid_names 枚举")
    fw_names = set(vr.get("six_flywheel_valid_names", []))
    missing = VALID_FLYWHEEL_NAMES - fw_names
    if missing:
        fail(f"six_flywheel_valid_names 缺少: {missing}")
    elif len(fw_names) == 6:
        ok(f"六飞轮枚举 6个全覆盖 ✓")
    else:
        fail(f"six_flywheel_valid_names 数量 {len(fw_names)} ≠ 6")

    # [7] aggregated_kpis 公式系数之和
    print("\n[6] aggregated_kpis 公式系数之和")
    formula = metrics.get("aggregated_kpis", {}).get("coach_performance_score", {}).get("formula", "")
    coeffs = [float(x) for x in re.findall(r'(\d+\.\d+)\s*\*', formula)]
    if coeffs:
        total = sum(coeffs)
        if abs(total - 1.0) < 1e-9:
            ok(f"公式系数之和 = {total:.2f} ✓ ({coeffs})")
        else:
            fail(f"公式系数之和 = {total:.4f} ≠ 1.0")
    else:
        fail("公式系数解析失败")

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
        print("  ✅ 教练有效性指标验证 PASS — 全部 KPI 配置合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
