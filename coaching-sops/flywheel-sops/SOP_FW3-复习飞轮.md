---
name: SOP_FW3-复习飞轮
description: 六飞轮第3飞轮:复习飞轮 SOP — 基于遗忘曲线的间隔复习体系
version: "1.0"
six_flywheel_id: 3
six_flywheel_name: 复习飞轮
stage_range: [2, 6]
license: Apache-2.0
tier: A
phase: "Phase 0"
status: stub
compliance: "v5.0 道层零漂移"
allowed-tools: [nuwa-skill, DeepTutor, gbrain]
---

# SOP_FW3 复习飞轮 — 间隔复习标准操作流程

## Use when
- 课后当天 / 3天后 / 7天后 / 30天后(四次复习周期)
- 学员处于第2阶(模糊)至第6阶(熟练)
- 知识点掌握度需要从"清晰"推进到"熟练"

## 核心目标
通过艾宾浩斯间隔复习,将工作记忆转化为长期记忆。

## 飞轮五步

1. **复习计划**: 根据遗忘曲线设定 [+1d, +3d, +7d, +30d] 复习提醒
2. **主动回忆**: 合上资料,用自己的话复述知识框架(SOP_03 输出)
3. **盲区定位**: 回忆中断处 = 薄弱点,标记并优先攻克
4. **框架更新**: 用新理解修正 SOP_03 的知识框架图
5. **掌握度标记**: 更新 stage_id(触发 promotion_event 时记录)

## 接口规范

```typescript
interface ReviewFlywheel {
  student_id: string;
  knowledge_point_id: string;
  review_cycle: 1 | 3 | 7 | 30;  // 天数
  recall_rate: number;             // 0-1 主动回忆成功率
  blind_spots: string[];
  stage_update: { from: number; to: number } | null;
  six_flywheel_id: 3;              // 复习飞轮
}
```

## 道层合规说明
- 六飞轮第3个="复习飞轮"(名称固定,不可更改)
