---
name: SOP_FW5-作业飞轮
description: 六飞轮第5飞轮:作业飞轮 SOP — 高质量作业执行与即时反馈闭环
version: "1.0"
six_flywheel_id: 5
six_flywheel_name: 作业飞轮
stage_range: [3, 6]
license: Apache-2.0
tier: A
phase: "Phase 0"
status: stub
compliance: "v5.0 道层零漂移"
allowed-tools: [nuwa-skill, DeepTutor, nanobot, OpenClaw]
---

# SOP_FW5 作业飞轮 — 作业执行闭环标准操作流程

## Use when
- 日常作业时间
- 学员处于第3阶(清晰)至第6阶(熟练)
- 需要提升作业质量,降低重复错误率

## 核心目标
将作业从"完成任务"转化为"诊断+提升"的双重价值。

## 飞轮五步

1. **作业审题**: 每题先用 SOP_04 完整审题(不跳步)
2. **流程执行**: 按 SOP_05 标准流程解题(第5步=流程)
3. **自批自改**: 完成后用 SOP_06 逻辑自批,错误即时归因
4. **薄弱标记**: 错题标记 knowledge_point_id + 错误类型(不是"错题本",是实时标记)
5. **当日总结**: 每日作业结束记录"今日暴露薄弱点",纳入 SOP_07 分析

## 接口规范

```typescript
interface HomeworkFlywheel {
  student_id: string;
  assignment_id: string;
  questions: Array<{
    question_id: string;
    outcome: "correct" | "incorrect" | "partial";
    error_type: "exam_reading" | "process" | "calculation" | "knowledge" | null;
    knowledge_point_id: string;
  }>;
  daily_weak_summary: string[];
  six_flywheel_id: 5;              // 作业飞轮
}
```

## 道层合规说明
- ⑤ = 流程(SOP_05) ✅ 道层合规
- 六飞轮无非法变体
