---
name: SOP_FW1-计划飞轮
description: |
  六飞轮第1飞轮:计划飞轮 SOP — 建立高质量学习计划执行体系。
  Use when 新学期或新阶段开始,或学员计划执行率低于60%。
version: "1.0"
six_flywheel_id: 1
six_flywheel_name: 计划飞轮
stage_range: [1, 7]
license: Apache-2.0
tier: A
phase: "Phase 0"
status: active
compliance: "v5.0 道层零漂移"
portal: xyt-coach
quadruple_context:
  six_flywheel_id: 1
  stage_range: [1, 7]
allowed-tools: [colleague-skill, nuwa-skill, gbrain]
---

# SOP_FW1 计划飞轮 — 计划制定与执行标准操作流程

## Use when
- 新学期/新阶段开始
- 学员无计划习惯或计划执行率 < 60%
- FIRE-UP 测评中 P(Pathways) 维度偏低

## 核心目标
帮助学员建立"计划→执行→复盘→迭代"的飞轮闭环。

## 飞轮五步

1. **目标拆解**: 将月目标拆分为周目标 → 日任务
2. **优先级排序**: 按"重要+紧急"四象限分配每日时间块
3. **执行记录**: 每日完成任务后打卡,记录实际用时
4. **偏差分析**: 每周比对计划 vs 实际,计算执行率
5. **计划迭代**: 基于偏差调整下周计划(≤30% 变动)

## 接口规范

```typescript
interface PlanningFlywheel {
  student_id: string;
  cycle: "weekly" | "monthly";
  goals: Array<{ goal_id: string; deadline: string; priority: 1|2|3|4 }>;
  tasks: Array<{ task_id: string; goal_id: string; planned_duration_min: number }>;
  completion_rate: number;       // 0-1
  six_flywheel_id: 1;            // 计划飞轮
}
```
