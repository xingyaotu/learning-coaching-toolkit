---
name: coach-1on1
description: |
  1V1 伴学课标准教练工作流 — 课前/课中/课后三段式结构化引导。
  Use when 教练开启1V1伴学课,需按八步学习法进行全程结构化教学指导。
version: "1.0"
colleague_skill_layer: work-skill
portal: xyt-coach
allowed-tools: [nuwa-skill, DeepTutor, nanobot]
quadruple_context:
  eight_step_ids: [1, 2, 3, 4, 5, 6, 7, 8]
  six_flywheel_ids: [1, 2, 3, 4, 5, 6]
compliance: "v5.0 道层零漂移"
---

# coach-1on1 · 1V1伴学课教练工作流

## 触发场景
- 1V1伴学课开始前5分钟准备
- 教练需要结构化执行八步学习法指导时
- 课后复盘与下次课准备

## 三段式结构

### 课前(5min) · 计划飞轮激活
1. 查看学员本周知识点卡点(七阶快照)
2. 确认本课目标知识点(≤2个)
3. 根据学员七阶位选择入口 SOP

### 课中(40min) · 八步核心执行

按学员当前七阶阶位选择入口:

| 七阶位 | 推荐步骤入口 | 对应 SOP |
|---|---|---|
| 1~2(不会/模糊) | ①穿透 → ②提取 | SOP_01 → SOP_02 |
| 3~4(清晰/框架) | ③整理 → ④审题 | SOP_03 → SOP_04 |
| 4~5(框架/运用) | ④审题 → ⑤流程 | SOP_04 → SOP_05 |
| 5~6(运用/熟练) | ⑥批改 → ⑦分析 | SOP_06 → SOP_07 |
| 7(创新) | ⑧估分 + 拓展 | SOP_08 |

### 课后(10min) · 复习飞轮触发
1. 生成课后总结(knowledge_point_id + stage_after)
2. 布置作业任务(参照作业飞轮 SOP_FW5)
3. 更新本周会话记录

## 接口参数

| 参数 | 类型 | 说明 |
|---|---|---|
| `student_id` | string | 学员ID |
| `session_date` | string | 课程日期 |
| `target_kp_ids` | string[] | 本课目标知识点ID |
| `coach_persona` | string? | 教练风格(见 colleague-skill/persona/) |

## 道层合规
- 八步第⑤步 = 流程(合规名称,见 dao-guard pattern 05)
- 六飞轮 = 计划/预习/复习/听课/作业/考试(标准6项)
- cso-required: 否
