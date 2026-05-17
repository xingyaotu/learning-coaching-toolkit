---
name: SOP_FW2-预习飞轮
description: 六飞轮第2飞轮:预习飞轮 SOP — 高效课前预习提升课堂吸收率
version: "1.0"
six_flywheel_id: 2
six_flywheel_name: 预习飞轮
stage_range: [1, 4]
license: Apache-2.0
tier: A
phase: "Phase 0"
status: stub
compliance: "v5.0 道层零漂移"
allowed-tools: [nuwa-skill, DeepTutor, nanobot]
---

# SOP_FW2 预习飞轮 — 课前预习标准操作流程

## Use when
- 课前30-60分钟
- 学员处于第1阶(不会)至第4阶(框架)
- 需要提升课堂效率

## 核心目标
课前建立知识框架骨架,使听课(FW4)效率提升40%以上。

## 飞轮五步

1. **扫描目录**: 快速浏览本节目录和标题,预判重点
2. **提取疑问**: 列出"不明白的地方"清单(配合 SOP_01 穿透)
3. **概念预估**: 对新概念做初步理解(哪怕是错的),为课堂修正留空
4. **框架草绘**: 画出本节知识框架草图(空框,待听课填充)
5. **时间记录**: 记录预习用时,纳入计划飞轮

## 接口规范

```typescript
interface PreviewFlywheel {
  student_id: string;
  chapter_id: string;
  questions_raised: string[];
  framework_sketch: string;     // 框架草图描述
  duration_min: number;
  six_flywheel_id: 2;            // 预习飞轮
}
```
