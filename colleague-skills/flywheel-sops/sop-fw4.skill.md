---
name: sop-fw4
description: |
  六飞轮第4飞轮:听课飞轮 SOP — 课堂主动参与最大化学习增益
  Use when 学员处于不会(1)至运用(5)阶;课堂注意力分散或被动接收;需建立带问题听课的主动参与机制
version: "1.0.0"
allowed-tools:
  - nuwa-skill
  - gbrain
  - Hermes
portal: xyt-coach
quadruple_context:
  six_flywheel_id: 4
  six_flywheel_name: 听课
  stage_range: [1, 5]
---

# SOP_FW4-听课飞轮

## 触发场景

- 学员当前七阶阶位 不会(1) 至 运用(5)
- 六飞轮第 4 飞轮「听课飞轮」激活时
- 道层对齐: 六飞轮 = 计划/预习/复习/听课/作业/考试 ✅

## 飞轮定位

| 飞轮编号 | 飞轮名称 | 阶位范围 |
|----------|----------|---------|
| 4 | 听课飞轮 | 不会(1) — 运用(5) |

## 调用规约

- 调用方式: `SOP_FW4` via colleague-skill 接口
- 参考文档: `coaching-sops/flywheel-sops/SOP_FW4-听课飞轮.md`
- 道层合规: 六飞轮枚举合规(计划/预习/复习/听课/作业/考试) ✅ | CSO 0触发 ✅
