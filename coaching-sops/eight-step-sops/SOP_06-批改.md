---
name: SOP_06-批改
description: 八步学习法第6步:作业批改 SOP — AI 辅助精准批改与错误归因
version: "1.0"
eight_step_id: 6
eight_step_name: 批改
primary_flywheel: 作业飞轮
flywheel_id: 5
stage_range: [4, 6]
license: Apache-2.0
tier: A
phase: "Phase 0"
status: stub
compliance: "v5.0 道层零漂移"
allowed-tools: [nuwa-skill, DeepTutor, OpenClaw, nanobot]
---

# SOP_06 批改 — 作业批改标准操作流程

## Use when
- 学员完成解题流程(SOP_05)后
- 处于第4阶(框架)至第6阶(熟练)
- 需要精准归因错误原因

## 核心目标
不仅判断对错,更要定位错误类型并触发阶段评估。

## 五步操作流程

1. **答案比对**: 与标准答案逐步核对
2. **错误分类**: 归类为 [审题错 / 流程错 / 计算错 / 知识错]
3. **知识点回溯**: 定位错误对应的 knowledge_point_id 和当前 stage_id
4. **阶段判断**: 若连续3次同类错误 → 触发降阶(demoted)
5. **反馈生成**: 输出针对性提示,建议回做 SOP_01 或 SOP_04

## 接口规范

```typescript
interface CorrectionSession {
  question_id: string;
  student_answer: string;
  correct_answer: string;
  error_type: "exam_reading" | "process" | "calculation" | "knowledge" | null;
  knowledge_point_id: string;
  stage_assessment: {
    current_stage: number;
    demotion_triggered: boolean;
    consecutive_errors: number;
  };
  outcome: "correct" | "incorrect" | "partial";
  eight_step_id: 6;
  six_flywheel_id: 5;            // 作业飞轮
}
```
