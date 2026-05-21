#!/usr/bin/env python3
# validate-sop-completeness.py v1.1
# 道层 Compliance: v5.1 | 验证 14 SOP 文件完整性
import json
import os
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
FAIL = False

EIGHT_STEP_SOPS = [
    'SOP_01-穿透.md', 'SOP_02-提取.md', 'SOP_03-整理.md', 'SOP_04-审题.md',
    'SOP_05-流程.md', 'SOP_06-批改.md', 'SOP_07-分析.md', 'SOP_08-估分.md'
]
FLYWHEEL_SOPS = [
    'SOP_FW1-计划飞轮.md', 'SOP_FW2-预习飞轮.md', 'SOP_FW3-复习飞轮.md',
    'SOP_FW4-听课飞轮.md', 'SOP_FW5-作业飞轮.md', 'SOP_FW6-考试飞轮.md'
]
COACH_OPS_SOPS = [
    'SOP_CO1-新生入学流程.md', 'SOP_CO2-每日伴读流程.md',
    'SOP_CO3-任务执行流程.md', 'SOP_CO4-沟通情绪处理.md'
]

print('=== SOP 完整性验证 v1.1 ===')

# 检查八步 SOPs
sop_dir = ROOT / 'coaching-sops'
for sop in EIGHT_STEP_SOPS:
    path = sop_dir / sop
    if not path.exists():
        print(f'❌ 缺失: {sop}')
        FAIL = True
    else:
        content = path.read_text(encoding='utf-8')
        if 'SOP_05' in sop and '演示' in content:
            print(f'❌ {sop} 含"演示"漂移词 — 八步⑤=流程')
            FAIL = True
        else:
            print(f'✅ {sop}')

# 检查飞轮 SOPs
for sop in FLYWHEEL_SOPS:
    path = sop_dir / sop
    if not path.exists():
        print(f'❌ 缺失: {sop}')
        FAIL = True
    else:
        print(f'✅ {sop}')

# 检查 coach-ops SOPs
cops_dir = sop_dir / 'coach-ops-sops'
for sop in COACH_OPS_SOPS:
    path = cops_dir / sop
    if not path.exists():
        print(f'❌ 缺失: {sop}')
        FAIL = True
    else:
        print(f'✅ {sop}')

# 检查 coaching-sops/index.json
index_path = sop_dir / 'index.json'
if not index_path.exists():
    print('❌ 缺失: coaching-sops/index.json')
    FAIL = True
else:
    try:
        with open(index_path, encoding='utf-8') as f:
            data = json.load(f)
        print('✅ coaching-sops/index.json 格式正确')
    except json.JSONDecodeError as e:
        print(f'❌ coaching-sops/index.json JSON 格式错误: {e}')
        FAIL = True

# 检查 pipeline-data/sop-skill-catalog.json
catalog_path = ROOT / 'pipeline-data' / 'sop-skill-catalog.json'
if not catalog_path.exists():
    print('❌ 缺失: pipeline-data/sop-skill-catalog.json')
    FAIL = True
else:
    try:
        with open(catalog_path, encoding='utf-8') as f:
            catalog = json.load(f)
        if '$schema' not in catalog:
            print('❌ sop-skill-catalog.json 缺少 $schema')
            FAIL = True
        else:
            print('✅ pipeline-data/sop-skill-catalog.json 含 $schema')
    except json.JSONDecodeError as e:
        print(f'❌ sop-skill-catalog.json JSON 格式错误: {e}')
        FAIL = True

print('')
if FAIL:
    print('❌ SOP 完整性验证 FAIL')
    sys.exit(1)
else:
    print('✅ SOP 完整性验证 PASS')
    sys.exit(0)
