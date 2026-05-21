---
name: coaching-toolkit-dispatcher
version: "1.0.0"
description: |
  教练工具包调度器。根据学员七阶位置、当前激活飞轮、八步焦点，
  路由至对应 SOP 文件并返回执行步骤。
portals: [xyt-coach]
use_when: |
  - 教练需要执行标准化操作流程时
  - 学员七阶位置发生变化需要调整策略时
  - 飞轮切换或任务布置时
  - 情绪/沟通异常需要处置时
cso_required: false
---

# coaching-toolkit-dispatcher

## 八步 SOP 调度表

| 八步编号 | 八步名称 | 对应 SOP | 触发条件 |
|---------|---------|---------|--------|
| ① | 穿透 | SOP_01-穿透.md | 新知识导入、诊断初始状态 |
| ② | 提取 | SOP_02-提取.md | 知识点归纳、错误提取 |
| ③ | 整理 | SOP_03-整理.md | 笔记整理、知识结构化 |
| ④ | 审题 | SOP_04-审题.md | 题目理解、审题训练 |
| ⑤ | 流程 | SOP_05-流程.md | 解题流程建立（绝非演示） |
| ⑥ | 批改 | SOP_06-批改.md | 作业批改、错误分析 |
| ⑦ | 分析 | SOP_07-分析.md | 学情分析、七阶评估 |
| ⑧ | 估分 | SOP_08-估分.md | 考前估分、考后复盘 |

## 六飞轮 SOP 调度表

| 飞轮 | 对应 SOP | 激活条件 |
|-----|---------|--------|
| 计划 | SOP_FW1-计划飞轮.md | 学期/周/日计划制定 |
| 预习 | SOP_FW2-预习飞轮.md | 课前预习任务布置 |
| 复习 | SOP_FW3-复习飞轮.md | 课后复习、错题回顾 |
| 听课 | SOP_FW4-听课飞轮.md | 课中陪伴、听课质量监控 |
| 作业 | SOP_FW5-作业飞轮.md | 作业布置与批改 |
| 考试 | SOP_FW6-考试飞轮.md | 考前准备、考后分析 |

## 教练运营 SOP 调度表

| 场景 | SOP | 触发条件 |
|-----|-----|--------|
| 新生入学 | SOP_CO1-新生入学流程.md | 学员首次接入，七阶 1-3 |
| 每日伴读 | SOP_CO2-每日伴读流程.md | 日常教练工作日执行 |
| 任务执行 | SOP_CO3-任务执行流程.md | 任务布置、跟进、批改 |
| 沟通情绪 | SOP_CO4-沟通情绪处理.md | 情绪抵触、沟通障碍 |

## 路由规则

```
if context == 'new_student' and stage in [1,2,3]:
    → SOP_CO1
elif context == 'daily_coaching':
    → SOP_CO2
elif context == 'task_issue' or flywheel in ['作业', '复习', '预习']:
    → SOP_CO3
elif context == 'emotion' or student_signal in ['抵触', '挫败', '焦虑']:
    → SOP_CO4
elif eight_step_focus in [1,2,3,4,5,6,7,8]:
    → SOP_{eight_step_focus:02d}-{eight_step_name}.md
elif flywheel in ['计划','预习','复习','听课','作业','考试']:
    → SOP_FW{flywheel_index}-{flywheel}.md
```

## 七阶适用映射

| 七阶 | 阶段名 | 推荐优先 SOP |
|-----|-------|-------------|
| 1 | 不会 | CO1 → CO3(A1) → SOP_01 |
| 2 | 模糊 | CO3 → SOP_02 → SOP_03 |
| 3 | 清晰 | SOP_04 → SOP_05 → CO3 |
| 4 | 框架 | SOP_05 → SOP_06 → FW3 |
| 5 | 运用 | SOP_06 → SOP_07 → FW5 |
| 6 | 熟练 | SOP_07 → SOP_08 → FW6 |
| 7 | 创新 | SOP_08 → FW6 → munger路由 |

## 道层合规声明

- 八步⑤=流程（绝非演示）✅
- 六飞轮：计划/预习/复习/听课/作业/考试（严格枚举）✅
- MECE=M-动力/E-执行力/C-能力/E-环境 ✅
- FIRE-UP=6字母 F/I/R/E/U/P ✅
- 七阶=不会/模糊/清晰/框架/运用/熟练/创新 ✅
