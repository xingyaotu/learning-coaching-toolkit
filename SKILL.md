---
name: coaching-sops-toolkit
description: |
  星耀途教练操作手册套件 — 14 个 SOP，覆盖八步教学法全流程与六飞轮激活策略。
  八步 SOP: 穿透(①) 提取(②) 整理(③) 审题(④) 流程(⑤) 批改(⑥) 分析(⑦) 估分(⑧)
  飞轮 SOP: 计划飞轮 / 预习飞轮 / 复习飞轮 / 听课飞轮 / 作业飞轮 / 考试飞轮
  Use when: 教练需要课前、课中、课后精确操作指导；学员卡点七阶诊断后 SOP 分发。
  Triggers: 教练操作手册 / 八步教学 / 飞轮激活 / SOP 查询 / 七阶诊断 / 学员卡点
version: "1.0.0"
portal: xyt-coach
source: xingyaotu/learning-coaching-toolkit
sop_index: coaching-sops/index.json
allowed-tools:
  - Read
---

# 教练操作手册套件 (coaching-sops-toolkit)

## 七阶 → SOP 分发矩阵

| 七阶位置 | 首选 SOP | 辅助 SOP | 推荐飞轮 |
|---|---|---|---|
| 1 不会 | SOP_01 穿透 | — | 预习飞轮 |
| 2 模糊 | SOP_01 穿透 | SOP_02 提取 | 预习飞轮 |
| 3 清晰 | SOP_02 提取 | SOP_03 整理 | 复习飞轮 |
| 4 框架 | SOP_04 审题 | SOP_05 流程 | 作业飞轮 |
| 5 运用 | SOP_05 流程 | SOP_06 批改 | 作业飞轮 |
| 6 熟练 | SOP_07 分析 | — | 复习飞轮 |
| 7 创新 | SOP_08 估分 | — | 考试飞轮 |

## 飞轮触发场景

| 飞轮 SOP | 触发时机 |
|---|---|
| SOP_FW1 计划飞轮 | 每周开始、月目标设定(全阶通用) |
| SOP_FW2 预习飞轮 | 新课前 24 小时内(七阶 1-4) |
| SOP_FW3 复习飞轮 | 课后 48 小时、周末强化(七阶 2-6) |
| SOP_FW4 听课飞轮 | 课中实时引导(七阶 1-5) |
| SOP_FW5 作业飞轮 | 作业布置与课后跟进(七阶 3-6) |
| SOP_FW6 考试飞轮 | 考前冲刺、考后复盘(七阶 4-7) |

## 调用接口

```
invoke coaching-sops-toolkit:
  stage_id:   int     # 1-7, 七阶位置
  sop_id:     string? # 直接指定 SOP_01..SOP_08, SOP_FW1..SOP_FW6
  subject:    string  # 科目
  student_id: string  # 学员 ID
```

读取对应 SOP:
```
Read coaching-sops/eight-step-sops/SOP_05-流程.md
Read coaching-sops/flywheel-sops/SOP_FW3-复习飞轮.md
Read coaching-sops/index.json
```

## 道层约束

- ⑤ = 流程(八步第5步唯一合法名称,绝无例外)
- 六飞轮 = 计划 / 预习 / 复习 / 听课 / 作业 / 考试(不得替换)
- FIRE-UP 6字母: F=Family / I=Individual / R=Resources / E=Ecosystem / U=Usability / P=Pathways
- cso-required: 否(纯操作指南,无 API key 引用)

## 集成说明

本套件在 xingyaotu-openmaic 的对接点:

- `agent-skills/coach/sop/` — 将 SOP SKILL 文件 vendor 至此目录
- `pipeline-data/coaching-tool-catalog.json` — 14 工具已收录
- 与 `precision-loop-analyst` 协作: 精准闭环分析后按七阶调用对应 SOP
- 与 `teaching-loop-builder` 协作: 教学闭环设计后按飞轮调用对应 SOP
