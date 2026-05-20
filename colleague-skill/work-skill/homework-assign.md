---
name: homework-assign
description: |
  每课作业布置标准工作流 — 按学员七阶位和当前薄弱点精准分配作业。
  Use when 教练课后布置作业,或系统自动生成周作业计划时触发。
version: "1.0"
colleague_skill_layer: work-skill
portal: xyt-coach
allowed-tools: [nuwa-skill, nanobot]
quadruple_context:
  eight_step_ids: [4, 5, 6]
  six_flywheel_ids: [5]
compliance: "v5.0 道层零漂移"
---

# homework-assign · 作业布置工作流

## 触发场景
- 每次伴学课结束后
- 作业飞轮(SOP_FW5)激活时
- 系统定时生成周作业计划

## 作业布置四步法

### 步骤1 · 审题训练选题

```
根据学员当前卡点知识点 + 七阶位:
  阶3~4 → 选择基础审题题组 (SOP_04 入口)
  阶5~6 → 选择综合审题题组 (SOP_04 高阶入口)
  来源: xkw.recommend(kp_id, stage)
```

### 步骤2 · 解题流程配置

按作业飞轮 SOP_FW5 标准执行:
- 每题先完成审题(SOP_04)
- 执行八步第5步(流程)解题标准
- 完成后自批(SOP_06逻辑)

### 步骤3 · 作业量校准

```
每日作业时间上限(分钟):
  小学: 30min
  初中: 45min
  高中: 60min
题量 = min(时间上限 / 平均解题时间, 5题)
```

### 步骤4 · 次日复盘节点

```
设置提醒: 次日课前检查作业完成情况
生成: 作业质量评分(正确率 + 解题规范性)
触发: 作业飞轮数据写入四元组动作记录
```

## 输出格式

```json
{
  "student_id": "{id}",
  "assignment_date": "{date}",
  "target_kp_ids": ["{kp_id}"],
  "question_sets": [{"uri": "xkw://...", "count": 3}],
  "estimated_minutes": 40,
  "flywheel_id": 5,
  "next_checkin": "{tomorrow}"
}
```

## 道层合规
- 八步第⑤步 = 流程(合规名称,见 dao-guard pattern 05)
- 六飞轮 = 计划/预习/复习/听课/作业/考试(标准6项)
- cso-required: 否
