---
name: sop-fw5
description: |
  六飞轮第5飞轮:作业飞轮 SOP — 将作业转化为高价值刻意练习
  Use when 学员处于清晰(3)至熟练(6)阶;作业完成质量低或仅追求完成率;需 SOP_04-SOP_06 闭环提升作业价值
version: "1.0.0"
allowed-tools:
  - nuwa-skill
  - gbrain
  - Hermes
  - colleague-skill
portal: xyt-coach
quadruple_context:
  six_flywheel_id: 5
  six_flywheel_name: 作业
  stage_range: [3, 6]
---

# SOP_FW5-作业飞轮

## 触发场景

- 学员当前七阶阶位 清晰(3) 至 熟练(6)
- 六飞轮第 5 飞轮「作业飞轮」激活时
- 道层对齐: 六飞轮 = 计划/预习/复习/听课/作业/考试 ✅

## 飞轮定位

| 飞轮编号 | 飞轮名称 | 阶位范围 |
|----------|----------|---------|
| 5 | 作业飞轮 | 清晰(3) — 熟练(6) |

## 调用规约

- 调用方式: `SOP_FW5` via colleague-skill 接口
- 参考文档: `coaching-sops/flywheel-sops/SOP_FW5-作业飞轮.md`
- 道层合规: 六飞轮枚举合规(计划/预习/复习/听课/作业/考试) ✅ | CSO 0触发 ✅
