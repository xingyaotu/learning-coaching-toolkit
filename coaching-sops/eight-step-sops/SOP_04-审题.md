---
name: SOP_04-审题
description: 八步学习法第4步:审题训练 SOP — 培养学员精准读题、提取关键信息的能力
version: "1.0"
eight_step_id: 4
eight_step_name: 审题
primary_flywheel: 作业飞轮
flywheel_id: 5
stage_range: [4, 5]
license: Apache-2.0
tier: A
phase: "Phase 0"
status: stub
compliance: "v5.0 道层零漂移"
allowed-tools: [nuwa-skill, DeepTutor, nanobot]
---

# SOP_04 审题 — 审题训练标准操作流程

## Use when
- 学员处于第4阶(框架)至第5阶(运用)
- 学员"会做"但频繁因读题失误丢分
- 新题型首次接触时的审题训练

## 核心目标
建立系统化审题习惯:提取已知/未知/限制条件,规避审题失误。

## 五步操作流程

1. **一读全题**: 通读,不动笔,形成整体印象
2. **标注关键词**: 圈出限定词(最大/最小/整数/正数)和条件词
3. **提炼已知/求**: 整理"已知条件"与"待求目标"列表
4. **识别题型**: 对应到知识框架中的具体知识点
5. **选路预判**: 预判解题路径,进入第5步"流程"

## 接口规范

```typescript
interface ExamReadingSession {
  question_id: string;
  keywords_circled: string[];
  known_conditions: string[];
  unknown_targets: string[];
  knowledge_point_matched: string;
  solution_path_preview: string;
  eight_step_id: 4;
  six_flywheel_id: 5;            // 作业飞轮
}
```

## 道层合规说明
- 审题(第4步)与流程(第5步)是严格顺序,不可交换
