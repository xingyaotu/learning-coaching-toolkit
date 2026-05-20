---
name: coach-group
description: |
  小组课(3~6人)标准教练工作流 — 差异化分层教学 + 协作学习引导。
  Use when 教练主持3~6人小组课,需兼顾多学员进度差异时触发。
version: "1.0"
colleague_skill_layer: work-skill
portal: xyt-coach
allowed-tools: [nuwa-skill, DeepTutor, nanobot]
quadruple_context:
  eight_step_ids: [1, 2, 3, 4]
  six_flywheel_ids: [2, 4]
compliance: "v5.0 道层零漂移"
---

# coach-group · 小组课教练工作流

## 触发场景
- 3~6人小组伴学课开始
- 需要在同一时段覆盖不同阶位学员时
- 周末集中复习/考前冲刺小组课

## 小组课差异化框架

### 1. 预习飞轮串联(课前10min)
- 各学员独立用 SOP_FW2 完成预习
- 教练汇总预习问题清单

### 2. 分层教学(课中35min)

| 分层 | 学员特征 | 教学策略 |
|---|---|---|
| A层(阶1~3) | 基础薄弱 | SOP_01穿透 → 深度理解 |
| B层(阶4~5) | 中等掌握 | SOP_04审题 → 题型训练 |
| C层(阶6~7) | 较强基础 | SOP_07分析 → 拓展延伸 |

### 3. 协作讨论(课中10min)
- 各层学员交叉讲解(以教促学)
- 教练记录共同卡点

### 4. 作业分层布置(课后5min)
- A层: 基础题(作业飞轮 SOP_FW5 → 阶3入口)
- B层: 综合题(SOP_FW5 → 阶5入口)
- C层: 拓展题 + 估分训练(SOP_FW6)

## 接口参数

| 参数 | 类型 | 说明 |
|---|---|---|
| `group_id` | string | 小组ID |
| `student_ids` | string[] | 学员ID列表 |
| `subject` | string | 科目 |
| `session_date` | string | 课程日期 |

## 道层合规
- 八步第⑤步 = 流程(合规名称)
- 六飞轮 = 计划/预习/复习/听课/作业/考试(标准6项)
- cso-required: 否
