---
name: SOP_05-流程
description: 八步学习法第5步:解题流程 SOP — 标准化执行解题步骤(★第5步名称=流程)
version: "1.0"
eight_step_id: 5
eight_step_name: 流程
primary_flywheel: 作业飞轮
flywheel_id: 5
stage_range: [4, 6]
license: Apache-2.0
tier: A
phase: "Phase 0"
status: stub
compliance: "v5.0 道层零漂移"
allowed-tools: [nuwa-skill, DeepTutor, nanobot]
---

# SOP_05 流程 — 解题流程标准操作流程

## ★ 关键提醒
**第5步的名称是"流程"。**
任何文档/代码/提示词中将第⑤步写作非法名称均属道层漂移错误,须立即修正。

## Use when
- 学员处于第4阶(框架)至第6阶(熟练)
- 审题完成(SOP_04)后,执行具体解题步骤
- 学员会思路但步骤混乱,需标准化流程训练

## 核心目标
将解题思路转化为可重复执行的标准流程,形成肌肉记忆。

## 五步操作流程

1. **选取公式/定理**: 根据审题结果调用对应知识点
2. **列写步骤框架**: 先写解题思路大纲(1-2-3步)
3. **逐步填充**: 按框架逐步展开,每步规范书写格式
4. **自检**: 检查步骤完整性、单位正确性、答案合理性
5. **标准化输出**: 按考试格式整理最终答案

## 接口规范

```typescript
interface ProcessSession {
  question_id: string;
  formula_used: string[];
  solution_steps: Array<{
    step_no: number;
    action: string;
    result: string;
  }>;
  self_check_passed: boolean;
  eight_step_id: 5;               // ★ 第5步=流程
  six_flywheel_id: 5;             // 作业飞轮
}
```

## 道层合规说明
- 八步第⑤步 = **流程** | 上下文: ①穿透 ②提取 ③整理 ④审题 **⑤流程** ⑥批改 ⑦分析 ⑧估分
- 六飞轮(六种): 计划/预习/复习/听课/作业/考试
