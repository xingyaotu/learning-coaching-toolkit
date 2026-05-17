---
name: SOP_FW4-听课飞轮
description: 六飞轮第4飞轮:听课飞轮 SOP — 最大化课堂学习效率的主动听课策略
version: "1.0"
six_flywheel_id: 4
six_flywheel_name: 听课飞轮
stage_range: [1, 5]
license: Apache-2.0
tier: A
phase: "Phase 0"
status: stub
compliance: "v5.0 道层零漂移"
allowed-tools: [nuwa-skill, colleague-skill]
---

# SOP_FW4 听课飞轮 — 课堂主动听课标准操作流程

## Use when
- 课堂进行中
- 学员处于第1阶(不会)至第5阶(运用)
- 需要提升课堂专注度和信息吸收率

## 核心目标
将课堂时间从"被动接收"转化为"主动构建知识框架"。

## 飞轮五步

1. **框架对照**: 带着 SOP_FW2(预习飞轮)的草图进教室,随时填充
2. **重点捕捉**: 关注老师强调3次以上的内容 → 标记为"高权重知识点"
3. **疑问即记**: 听不懂立即标注,不打断思路,课后用 SOP_01 攻克
4. **例题跟做**: 老师例题同步用 SOP_04+SOP_05 流程自己做一遍
5. **课后5分钟**: 课程结束立即复述本节3个核心知识点,触发 SOP_FW3 周期

## 接口规范

```typescript
interface ClassFlywheel {
  student_id: string;
  class_id: string;
  framework_filled_percent: number;  // 课前草图被填充的比例
  high_weight_points: string[];
  questions_noted: string[];
  post_class_recap: string[];         // 3个核心知识点
  six_flywheel_id: 4;                 // 听课飞轮
}
```
