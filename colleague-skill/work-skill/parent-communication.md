---
name: parent-communication
description: |
  家长沟通标准工作流 — 周度进度反馈 + 月度家长课 + 里程碑汇报。
  Use when 教练需要向家长汇报学员学习进展,或触发家长沟通节点时。
version: "1.0"
colleague_skill_layer: work-skill
portal: xyt-coach
allowed-tools: [nuwa-skill, nanobot]
quadruple_context:
  eight_step_ids: [7, 8]
  six_flywheel_ids: [1, 6]
compliance: "v5.0 道层零漂移"
---

# parent-communication · 家长沟通工作流

## 触发场景
- 每周五发送周报
- 每月月底月家长课(SOP_W03)
- 学员七阶突破里程碑时

## 三类沟通模板

### 1. 周度进展报告(自动生成)

数据来源: SOP_07(错题分析) + SOP_08(估分复盘)

```
内容结构:
  - 本周知识点阶位变化: +{N}个知识点晋级
  - 当前薄弱知识点: TOP-3 卡点
  - 六大飞轮本周激活情况
  - 下周计划(教练备注)
```

### 2. 月度家长课准备

```
内容:
  - 30天知识点掌握趋势图
  - 与同期学员对比(匿名)
  - 下月阶段性目标设定
  - 家长配合要点
```

### 3. 里程碑推送

触发条件:
- 学员某知识点达到阶7(创新)
- 六飞轮全部激活首次
- 月均晋级≥5个知识点

## 沟通规范
- 聚焦数据和具体行动建议
- 避免只给定性描述(如"进步很大")
- 每次沟通明确"下一步行动"

## 道层合规
- 六飞轮 = 计划/预习/复习/听课/作业/考试(标准6项)
- cso-required: 否(学员进展数据汇报须脱敏)
