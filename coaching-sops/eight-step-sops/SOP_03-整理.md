---
name: SOP_03-整理
description: |
  八步学习法第3步:知识框架整理 SOP — 将提取的知识点组织为结构化框架。
  Use when 学员处于第3-4阶(清晰/框架),已理解知识点需整理形成体系。
version: "1.0"
eight_step_id: 3
eight_step_name: 整理
primary_flywheel: 复习飞轮
flywheel_id: 3
stage_range: [3, 4]
license: Apache-2.0
tier: A
phase: "Phase 0"
status: active
compliance: "v5.0 道层零漂移"
portal: xyt-coach
quadruple_context:
  eight_step_id: 3
  six_flywheel_id: 3
  stage_range: [3, 4]
allowed-tools: [nuwa-skill, DeepTutor, gbrain]
---

# SOP_03 整理 — 知识框架整理标准操作流程

## Use when
- 学员处于第3阶(清晰)至第4阶(框架)
- 已完成"提取",需要将知识点组织成框架
- 学员知识点零散,无法形成系统认知

## 核心目标
将零散知识点重组为层次清晰的框架树,支撑后续"运用"。

## 五步操作流程

1. **分类聚合**: 将相关知识点归类(概念/公式/方法/原理)
2. **框架构建**: 绘制思维导图或层级大纲
3. **关联梳理**: 标明知识点间的逻辑关系(并列/递进/因果)
4. **框架检验**: 用3个测试题验证框架覆盖度
5. **框架固化**: 输出可复用的"单元知识框架卡"

## 接口规范

```typescript
interface OrganizationSession {
  input_points: string[];        // 来自 SOP_02 的知识点 ID 列表
  framework: {
    title: string;
    nodes: Array<{ id: string; children: string[]; relation: "parallel"|"sequence"|"causal" }>;
  };
  coverage_test_count: 3;
  eight_step_id: 3;
  six_flywheel_id: 3;            // 复习飞轮
}
```

## 道层合规说明
- 六飞轮第3个="复习飞轮"(不是"总结飞轮")
