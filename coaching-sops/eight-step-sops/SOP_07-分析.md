---
name: SOP_07-分析
description: |
  八步学习法第7步:试卷分析 SOP — 系统性分析学习数据,识别薄弱点。
  Use when 学员处于第5-7阶(运用/熟练/创新),考后需深度分析失分点。
version: "1.0"
eight_step_id: 7
eight_step_name: 分析
primary_flywheel: 考试飞轮
flywheel_id: 6
stage_range: [5, 7]
license: Apache-2.0
tier: A
phase: "Phase 0"
status: active
compliance: "v5.0 道层零漂移"
portal: xyt-coach
quadruple_context:
  eight_step_id: 7
  six_flywheel_id: 6
  stage_range: [5, 7]
allowed-tools: [nuwa-skill, gbrain, Hermes]
---

# SOP_07 分析 — 学习数据分析标准操作流程

## Use when
- 阶段考试/模拟卷完成后
- 学员处于第5阶(运用)至第7阶(创新)
- 需要系统诊断薄弱知识点

## 核心目标
从批改数据中提炼规律性薄弱点,生成个性化改进计划。

## 五步操作流程

1. **数据聚合**: 收集最近N次作业/考试的 quadruple 记录
2. **薄弱点识别**: 按 knowledge_point_id 聚合错误率,阈值 > 40% 标红
3. **阶段分布分析**: 分析各知识点的 stage_id 分布,定位停滞点
4. **飞轮匹配**: 将薄弱点与最对应的飞轮挂钩(为第8步估分准备)
5. **改进计划**: 输出"本周重点攻克知识点 TOP5"和对应 SOP 建议

## 接口规范

```typescript
interface AnalysisSession {
  student_id: string;
  analysis_window_days: number;
  weak_points: Array<{
    knowledge_point_id: string;
    error_rate: number;
    current_stage: number;
    recommended_sop: string;
  }>;
  flywheel_gaps: Record<string, number>;  // flywheel_id → gap_score
  improvement_plan: string[];
  eight_step_id: 7;
  six_flywheel_id: 6;            // 考试飞轮
}
```
