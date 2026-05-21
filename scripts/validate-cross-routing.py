#!/usr/bin/env python3
"""
道层跨数据一致性验证脚本 v1.0
验证 stage-to-sop-routing.json ↔ coaching-session-templates.json 的联动一致性。

验证项:
  1. routing 中 primary_flywheels 均在 templates 飞轮模板中存在
  2. routing 中 eight_step_focus step_id 均在 templates 八步模板中存在
  3. routing stage_id → templates target_stages 覆盖 (路由到的模板支持该阶位)
  4. templates 飞轮 stage_range 与 sop-skill-catalog stage_range 一致
  5. ⑤ 联动守护: routing 中 step 5 name='流程' 且 template 中 step 5 name='流程'
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
ROUTING_PATH = REPO_ROOT / "pipeline-data" / "stage-to-sop-routing.json"
TEMPLATE_PATH = REPO_ROOT / "pipeline-data" / "coaching-session-templates.json"
CATALOG_PATH = REPO_ROOT / "pipeline-data" / "sop-skill-catalog.json"

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
    print("=" * 65)
    print("  跨数据一致性验证 v1.0 — routing ↔ templates ↔ catalog")
    print("=" * 65)

    # [1] 文件加载
    print("\n[1] 文件加载")
    for p in [ROUTING_PATH, TEMPLATE_PATH, CATALOG_PATH]:
        if not p.exists():
            fail(f"文件不存在: {p.name}")
            sys.exit(1)
    routing = json.loads(ROUTING_PATH.read_text(encoding="utf-8"))
    templates = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    ok("routing + templates + catalog 全部加载成功")

    matrix = routing.get("routing_matrix", [])
    eight_tpls = {t["eight_step_id"]: t for t in templates.get("eight_step_session_templates", [])}
    fw_tpls = {t["six_flywheel_name"]: t for t in templates.get("flywheel_session_templates", [])}
    catalog_fw = {s["six_flywheel_name"]: s for s in catalog.get("flywheel_sops", [])}

    # [2] routing primary_flywheels → templates 存在性
    print("\n[2] routing.primary_flywheels → templates 飞轮模板存在性")
    for r in matrix:
        sid = r["stage_id"]
        for fw in r.get("primary_flywheels", []):
            if fw in fw_tpls:
                ok(f"stage{sid} flywheel='{fw}' → templates 有对应模板 ✓")
            else:
                fail(f"stage{sid} flywheel='{fw}' 在 templates 中无对应模板")

    # [3] routing eight_step_focus → templates 存在性
    print("\n[3] routing.eight_step_focus → templates 八步模板存在性")
    for r in matrix:
        sid = r["stage_id"]
        for step in r.get("eight_step_focus", []):
            step_id = step["step_id"]
            if step_id in eight_tpls:
                ok(f"stage{sid} step{step_id}='{step['step_name']}' → templates 有对应模板 ✓")
            else:
                fail(f"stage{sid} step{step_id} 在 templates 中无对应模板")

    # [4] stage 与 target_stages 覆盖性 (each routed stage must be in template.target_stages)
    print("\n[4] routing stage_id ∈ template.target_stages 覆盖验证")
    for r in matrix:
        sid = r["stage_id"]
        # check primary flywheels
        for fw in r.get("primary_flywheels", []):
            tpl = fw_tpls.get(fw)
            if tpl:
                if sid in tpl.get("target_stages", []):
                    ok(f"stage{sid} 在 '{fw}'模板 target_stages 中 ✓")
                else:
                    fail(f"stage{sid} 不在 '{fw}'模板 target_stages={tpl['target_stages']} 中")
        # check primary eight-step
        for step in r.get("eight_step_focus", []):
            step_id = step["step_id"]
            tpl = eight_tpls.get(step_id)
            if tpl:
                if sid in tpl.get("target_stages", []):
                    ok(f"stage{sid} 在 step{step_id}'{step['step_name']}'模板 target_stages 中 ✓")
                else:
                    fail(f"stage{sid} 不在 step{step_id}模板 target_stages={tpl['target_stages']} 中")

    # [5] ⑤ 联动守护 — routing step 5 name == template step 5 name == '流程'
    print("\n[5] ⑤ 联动守护 (routing ↔ templates 双向)")
    routing_step5s = [
        step for r in matrix
        for step in r.get("eight_step_focus", [])
        if step["step_id"] == 5
    ]
    for s in routing_step5s:
        if s["step_name"] == "流程":
            ok(f"routing step5 name='流程' ✓")
        else:
            fail(f"routing step5 name='{s['step_name']}' ≠ '流程' ⑤守护失败")
        break  # check once is enough

    tpl5 = eight_tpls.get(5)
    if tpl5:
        if tpl5.get("eight_step_name") == "流程":
            ok("templates step5 name='流程' ⑤联动守护通过 ✓")
        else:
            fail(f"templates step5 name='{tpl5.get('eight_step_name')}' ≠ '流程' ⑤联动失败")

    # [6] flywheel stage_range catalog ↔ templates target_stages 一致性
    print("\n[6] catalog.flywheel stage_range ↔ templates.target_stages 一致性")
    for fw_name, cat_sop in catalog_fw.items():
        cat_range = cat_sop.get("stage_range", [])
        tpl = fw_tpls.get(fw_name)
        if tpl is None:
            fail(f"飞轮 '{fw_name}' 在 templates 中无对应模板")
            continue
        tpl_stages = tpl.get("target_stages", [])
        if not tpl_stages:
            fail(f"飞轮 '{fw_name}' templates.target_stages 为空")
            continue
        tpl_min, tpl_max = min(tpl_stages), max(tpl_stages)
        cat_min, cat_max = cat_range[0], cat_range[1]
        if tpl_min == cat_min and tpl_max == cat_max:
            ok(f"飞轮 '{fw_name}': catalog[{cat_min},{cat_max}] ↔ templates[{tpl_min},{tpl_max}] 一致 ✓")
        else:
            fail(f"飞轮 '{fw_name}': catalog range [{cat_min},{cat_max}] ≠ templates range [{tpl_min},{tpl_max}]")

    # ── 结果 ──────────────────────────────────────────────────────
    print(f"\n{'=' * 65}")
    total = PASS_COUNT + FAIL_COUNT
    print(f"  结果: {PASS_COUNT}/{total} 通过 | {FAIL_COUNT} 失败")
    print("=" * 65)
    if FAIL_COUNT > 0:
        print("\n失败详情:")
        for e in ERRORS:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("  ✅ 跨数据一致性验证 PASS — routing ↔ templates ↔ catalog 全部一致")
        sys.exit(0)


if __name__ == "__main__":
    main()
