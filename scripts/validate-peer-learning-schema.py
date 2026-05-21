#!/usr/bin/env python3
"""
道层教练同伴学习 schema 验证脚本 v1.0
验证 pipeline-data/coaching-peer-learning-schema.json 的合规性。

验证项:
  1. JSON 文件加载
  2. peer_pair_schema: 6个必填字段
  3. pairing_basis enum + _dao_guard 含'七阶'+'MECE'+'六飞轮'
  4. stage_at_pairing_a enum 七阶 + _dao_guard 含'七阶'
  5. flywheel_focus enum 六飞轮 + _dao_guard 含'六飞轮'
  6. sop05_peer_check_enabled _dao_guard 含'流程' ⑤守护
  7. peer_session_record_schema: stage_observed_a enum 七阶 + _dao_guard
  8. peer_session_record_schema: flywheel_practiced enum 六飞轮 + _dao_guard
  9. peer_session_record_schema: sop05_peer_check_result _dao_guard 含'流程'
  10. peer_learning_effectiveness: flywheel_improvement_rates 六飞轮 + _dao_guard
  11. peer_learning_effectiveness: sop05_peer_check_pass_rate ⑤守护
  12. peer_learning_effectiveness: stage_advance_due_to_peer _dao_guard 含'七阶'
  13. validation_rules: sop05_guard/七阶/MECE/六飞轮/pipl
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PEER_PATH = REPO_ROOT / "pipeline-data" / "coaching-peer-learning-schema.json"

VALID_FLYWHEEL_NAMES = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STAGE_NAMES = {"不会", "模糊", "清晰", "框架", "运用", "熟练", "创新"}
MECE_DIMENSIONS = {"M", "E_exec", "C", "E_env"}
REQUIRED_PAIR_FIELDS = {
    "pair_id", "student_a_id", "student_b_id",
    "initiating_coach_id", "pair_start_date", "pair_status"
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
    print("  教练同伴学习 schema 验证 v1.0")
    print("=" * 62)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not PEER_PATH.exists():
        fail(f"找不到文件: {PEER_PATH}")
        sys.exit(1)
    data = json.loads(PEER_PATH.read_text(encoding="utf-8"))
    ok("coaching-peer-learning-schema.json 加载成功")

    pp_fields = data.get("peer_pair_schema", {}).get("fields", {})
    ps_fields = data.get("peer_session_record_schema", {}).get("fields", {})
    ple_fields = data.get("peer_learning_effectiveness", {}).get("fields", {})
    vr = data.get("validation_rules", {})

    # [2] peer_pair_schema 6个必填字段
    print("\n[2] peer_pair_schema 6个必填字段")
    for fname in REQUIRED_PAIR_FIELDS:
        if fname in pp_fields:
            ok(f"peer_pair_schema.fields.{fname} 存在 ✓")
        else:
            fail(f"peer_pair_schema.fields.{fname} 缺失")

    # [3] pairing_basis enum + _dao_guard 含'七阶'+'MECE'+'六飞轮'
    print("\n[3] pairing_basis enum + _dao_guard 含'七阶'+'MECE'+'六飞轮'")
    pb_field = pp_fields.get("pairing_basis", {})
    pb_enum = set(pb_field.get("enum", []))
    expected_pb = {"pb-stage-peer", "pb-bottleneck-complement", "pb-flywheel-share", "pb-coach-assigned"}
    if pb_enum == expected_pb:
        ok("pairing_basis enum 四种配对依据 ✓")
    else:
        fail(f"pairing_basis enum {pb_enum} ≠ {expected_pb}")
    pb_guard = pb_field.get("_dao_guard", "")
    if "七阶" in pb_guard and "MECE" in pb_guard and "六飞轮" in pb_guard:
        ok("pairing_basis._dao_guard 含'七阶'+'MECE'+'六飞轮' ✓")
    else:
        fail(f"pairing_basis._dao_guard='{pb_guard}' 未含全部关键词")

    # [4] stage_at_pairing_a enum 七阶 + _dao_guard
    print("\n[4] stage_at_pairing_a enum 七阶 + _dao_guard")
    spa_field = pp_fields.get("stage_at_pairing_a", {})
    spa_enum = set(spa_field.get("enum", []))
    if spa_enum == VALID_STAGE_NAMES:
        ok("stage_at_pairing_a enum 七阶全覆盖 ✓")
    else:
        fail(f"stage_at_pairing_a enum {spa_enum} ≠ {VALID_STAGE_NAMES}")
    spa_guard = spa_field.get("_dao_guard", "")
    if "七阶" in spa_guard:
        ok("stage_at_pairing_a._dao_guard 含'七阶' ✓")
    else:
        fail(f"stage_at_pairing_a._dao_guard='{spa_guard}' 未含'七阶'")

    # [5] flywheel_focus enum 六飞轮 + _dao_guard
    print("\n[5] flywheel_focus enum 六飞轮 + _dao_guard")
    ff_field = pp_fields.get("flywheel_focus", {})
    ff_enum = set(ff_field.get("enum", []))
    if ff_enum == VALID_FLYWHEEL_NAMES:
        ok("flywheel_focus enum 六飞轮全覆盖 ✓")
    else:
        fail(f"flywheel_focus enum {ff_enum} ≠ {VALID_FLYWHEEL_NAMES}")
    ff_guard = ff_field.get("_dao_guard", "")
    if "六飞轮" in ff_guard:
        ok("flywheel_focus._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"flywheel_focus._dao_guard='{ff_guard}' 未含'六飞轮'")

    # [6] sop05_peer_check_enabled ⑤守护
    print("\n[6] sop05_peer_check_enabled ⑤守护 含'流程'")
    sop_guard = pp_fields.get("sop05_peer_check_enabled", {}).get("_dao_guard", "")
    if "流程" in sop_guard:
        ok("sop05_peer_check_enabled._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_peer_check_enabled._dao_guard='{sop_guard}' 未含'流程'")

    # [7] peer_session: stage_observed_a enum 七阶 + _dao_guard
    print("\n[7] peer_session_record stage_observed_a enum 七阶 + _dao_guard")
    soa_field = ps_fields.get("stage_observed_a", {})
    soa_enum = set(soa_field.get("enum", []))
    if soa_enum == VALID_STAGE_NAMES:
        ok("stage_observed_a enum 七阶全覆盖 ✓")
    else:
        fail(f"stage_observed_a enum {soa_enum} ≠ {VALID_STAGE_NAMES}")
    soa_guard = soa_field.get("_dao_guard", "")
    if "七阶" in soa_guard:
        ok("stage_observed_a._dao_guard 含'七阶' ✓")
    else:
        fail(f"stage_observed_a._dao_guard='{soa_guard}' 未含'七阶'")

    # [8] peer_session: flywheel_practiced enum 六飞轮 + _dao_guard
    print("\n[8] peer_session_record flywheel_practiced enum 六飞轮 + _dao_guard")
    fwp_field = ps_fields.get("flywheel_practiced", {})
    fwp_enum = set(fwp_field.get("enum", []))
    if fwp_enum == VALID_FLYWHEEL_NAMES:
        ok("flywheel_practiced enum 六飞轮全覆盖 ✓")
    else:
        fail(f"flywheel_practiced enum {fwp_enum} ≠ {VALID_FLYWHEEL_NAMES}")
    fwp_guard = fwp_field.get("_dao_guard", "")
    if "六飞轮" in fwp_guard:
        ok("flywheel_practiced._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"flywheel_practiced._dao_guard='{fwp_guard}' 未含'六飞轮'")

    # [9] peer_session: sop05_peer_check_result ⑤守护
    print("\n[9] peer_session_record sop05_peer_check_result ⑤守护 含'流程'")
    sprc_guard = ps_fields.get("sop05_peer_check_result", {}).get("_dao_guard", "")
    if "流程" in sprc_guard:
        ok("sop05_peer_check_result._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_peer_check_result._dao_guard='{sprc_guard}' 未含'流程'")

    # [10] flywheel_improvement_rates 六飞轮 + _dao_guard
    print("\n[10] peer_learning_effectiveness flywheel_improvement_rates 六飞轮 + _dao_guard")
    fir_field = ple_fields.get("flywheel_improvement_rates", {})
    fir_props = set(fir_field.get("properties", {}).keys())
    if fir_props == VALID_FLYWHEEL_NAMES:
        ok("flywheel_improvement_rates 六飞轮全覆盖 ✓")
    else:
        fail(f"flywheel_improvement_rates {fir_props} ≠ {VALID_FLYWHEEL_NAMES}")
    fir_guard = fir_field.get("_dao_guard", "")
    if "六飞轮" in fir_guard:
        ok("flywheel_improvement_rates._dao_guard 含'六飞轮' ✓")
    else:
        fail(f"flywheel_improvement_rates._dao_guard='{fir_guard}' 未含'六飞轮'")

    # [11] sop05_peer_check_pass_rate ⑤守护
    print("\n[11] peer_learning_effectiveness sop05_peer_check_pass_rate ⑤守护")
    spcpr_guard = ple_fields.get("sop05_peer_check_pass_rate", {}).get("_dao_guard", "")
    if "流程" in spcpr_guard:
        ok("sop05_peer_check_pass_rate._dao_guard 含'流程' ⑤守护 ✓")
    else:
        fail(f"sop05_peer_check_pass_rate._dao_guard='{spcpr_guard}' 未含'流程'")

    # [12] stage_advance_due_to_peer _dao_guard 含'七阶'
    print("\n[12] peer_learning_effectiveness stage_advance_due_to_peer _dao_guard 含'七阶'")
    sadp_guard = ple_fields.get("stage_advance_due_to_peer", {}).get("_dao_guard", "")
    if "七阶" in sadp_guard:
        ok("stage_advance_due_to_peer._dao_guard 含'七阶' ✓")
    else:
        fail(f"stage_advance_due_to_peer._dao_guard='{sadp_guard}' 未含'七阶'")

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
        print("  ✅ 教练同伴学习 schema 验证 PASS — 配对字段/⑤守护/七阶/MECE/六飞轮/PIPL 全合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
