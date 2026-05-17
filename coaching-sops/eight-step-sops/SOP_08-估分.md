---
name: SOP_08-估分
description: 八步学习法第8步:考前估分 SOP — 基于IRT与历史数据预测考试得分
version: "1.0"
eight_step_id: 8
eight_step_name: 估分
primary_flywheel: 考试飞轮
flywheel_id: 6
stage_range: [5, 7]
license: Apache-2.0
tier: A
phase: "Phase 0"
status: stub
compliance: "v5.0 道层零漂移"
allowed-tools: [nuwa-skill, gbrain, Hermes, nanobot]
---

# SOP_08 估分 — 考前估分标准操作流程

## Use when
- 大考前1-2周
- 学员处于第5阶(运用)至第7阶(创新)
- 需要制定考前冲刺计划

## 核心目标
基于知识点掌握度矩阵,预测各题型得分并生成冲刺建议。

## 五步操作流程

1. **掌握度快照**: 获取所有考纲知识点的当前 stage_id
2. **题型权重映射**: 将知识点映射到考试题型和对应分值
3. **IRT 得分预测**: 基于 stage_id + IRT 参数计算各题通过概率
4. **总分区间估算**: 输出 [P10, P50, P90] 三档得分预测
5. **冲刺清单**: 识别"多努力1周可提10分"的知识点,输出优先级清单

## 接口规范

```typescript
interface ScorePredictionSession {
  student_id: string;
  exam_syllabus_points: string[];
  stage_snapshot: Record<string, number>; // knowledge_point_id → stage_id
  score_prediction: {
    p10: number;
    p50: number;
    p90: number;
    total_possible: number;
  };
  sprint_targets: Array<{
    knowledge_point_id: string;
    current_stage: number;
    target_stage: number;
    estimated_score_gain: number;
  }>;
  eight_step_id: 8;
  six_flywheel_id: 6;            // 考试飞轮
}
```

## 道层合规说明
- 第8步"估分"是八步最后一步,与考试飞轮强绑定
- FIRE-UP 6 维中的 P=Pathways(成长路径)对此有直接影响
