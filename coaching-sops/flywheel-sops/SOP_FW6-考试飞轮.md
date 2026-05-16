---
name: SOP_FW6-考试飞轮
description: 六飞轮第6飞轮:考试飞轮 SOP — 考前冲刺、考中策略、考后分析三段闭环
version: "1.0"
six_flywheel_id: 6
six_flywheel_name: 考试飞轮
stage_range: [4, 7]
license: Apache-2.0
tier: A
phase: "Phase 0"
status: stub
compliance: "v5.0 道层零漂移"
allowed-tools: [nuwa-skill, gbrain, Hermes, colleague-skill]
---

# SOP_FW6 考试飞轮 — 考试全周期标准操作流程

## Use when
- 考试前2周(冲刺段)
- 考试当天(考中策略)
- 考试后48小时内(考后分析)
- 学员处于第4阶(框架)至第7阶(创新)

## 核心目标
将每次考试转化为"诊断+提升"的学习飞轮,而非单纯成绩测量。

## 飞轮三段五步

### 考前段
1. **估分建模**: 用 SOP_08 生成 [P10/P50/P90] 得分预测
2. **冲刺聚焦**: 依 SOP_08 的冲刺清单,重点攻克高ROI知识点

### 考中段
3. **时间分配**: 按题型分值/难度分配答题时间,高分题优先保分

### 考后段
4. **即时估分**: 考后30分钟内自估各大题得分
5. **误差分析**: 实际得分出来后,与 SOP_08 预测比对,修正 IRT 参数

## 接口规范

```typescript
interface ExamFlywheel {
  student_id: string;
  exam_id: string;
  phase: "pre_exam" | "during_exam" | "post_exam";
  score_prediction?: { p10: number; p50: number; p90: number };
  actual_score?: number;
  prediction_error?: number;
  irt_calibration_needed: boolean;
  knowledge_gaps_identified: string[];
  six_flywheel_id: 6;              // 考试飞轮
}
```

## 道层合规说明
- 六飞轮最后一个="考试飞轮"(不是"冲刺飞轮")
- FIRE-UP 6 维 F=Family/I=Individual/R=Resources/E=Ecosystem/U=Usability/P=Pathways
