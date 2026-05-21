---
name: SOP_02-提取
description: 八步学习法第2步:知识点提取 SOP — 从材料中精准提取核心知识结构
version: "1.0"
eight_step_id: 2
eight_step_name: 提取
primary_flywheel: 预习飞轮
flywheel_id: 2
stage_range: [2, 4]
license: Apache-2.0
tier: A
phase: "Phase 0"
status: stub
compliance: "v5.0 道层零漂移"
allowed-tools: [nuwa-skill, DeepTutor, nanobot]
---

# SOP_02 提取 — 知识点提取标准操作流程

## Use when
- 学员处于第2阶(模糊)至第4阶(框架)
- 面对新章节/单元,需要建立知识点清单
- 学员能理解但无法独立整理知识结构

## 核心目标
从教材/讲义中精准提取知识点,构建原始清单。

## 五步操作流程

1. **材料扫描**: 快速浏览全章,标记粗体/公式/定义
2. **知识点命名**: 为每个知识点赋予标准 knowledge_point_id 格式
3. **层级判断**: 区分主干知识点(必考)与支干知识点(拓展)
4. **关联标注**: 标记知识点间的前置/后置依赖关系
5. **清单输出**: 生成结构化知识点清单,为第3步"整理"备料

## 接口规范

```typescript
interface ExtractionSession {
  source_material: string;       // 教材章节 ID
  extracted_points: Array<{
    knowledge_point_id: string;
    level: "main" | "branch";
    prerequisites: string[];
  }>;
  eight_step_id: 2;
  six_flywheel_id: 2;            // 预习飞轮
}
```

## 道层合规说明
- 八步第2步="提取",不得替换为"摘录"或"笔记"
- 六飞轮无"笔记"型飞轮
