---
name: SOP_01-穿透
description: 八步学习法第1步:概念穿透 SOP — 帮助学员突破表层记忆,深度理解知识点本质
version: "1.0"
eight_step_id: 1
eight_step_name: 穿透
primary_flywheel: 预习飞轮
flywheel_id: 2
stage_range: [1, 3]
license: Apache-2.0
tier: A
phase: "Phase 0"
status: stub
compliance: "v5.0 道层零漂移"
allowed-tools: [nuwa-skill, DeepTutor, nanobot]
---

# SOP_01 穿透 — 概念穿透标准操作流程

## Use when
- 学员处于第1阶(不会)至第3阶(清晰)
- 知识点首次接触或掌握度 < 清晰
- 学员能背公式但解不了题(表层记忆)

## 核心目标
让学员从"背"到"懂":理解知识点的来源、本质和边界。

## 五步操作流程

1. **提问触发**: 用"为什么"而非"是什么"引导 — "这个公式是怎么来的?"
2. **类比映射**: 将抽象概念映射到学员熟悉的具体场景
3. **边界测试**: 给出反例,明确知识点的适用条件
4. **本质陈述**: 要求学员用自己的话表述知识点的本质(≤2句)
5. **应用预告**: 预告该知识点在八步第2步"提取"中的角色

## 接口规范(与 nuwa-skill 对接)

```typescript
interface PenetrationSession {
  knowledge_point_id: string;
  stage_before: 1 | 2 | 3;
  analog_used: string;          // 类比描述
  boundary_cases: string[];     // 边界反例
  student_essence_statement: string; // 学员本质陈述
  stage_after: 1 | 2 | 3;
  eight_step_id: 1;             // 固定为 1
  six_flywheel_id: 2;           // 预习飞轮
}
```

## 道层合规说明
- ⑤ = 流程(本 SOP 为步骤①,八步中⑤绝不是"演示")
- 六飞轮: 计划/预习/复习/听课/作业/考试(无非法变体)
