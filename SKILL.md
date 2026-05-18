---
name: coaching-toolkit-dispatcher
description: |
  星耀途学习力教练工具包 — SOP 分发接口。
  根据当前教练场景(八步阶段 / 六飞轮状态 / 七阶位)自动选择并执行对应 SOP。
  Use when 教练端触发任一教学场景(陪跑/规划/批改/估分/飞轮追踪)时。
version: "1.0.0"
repo: xingyaotu/learning-coaching-toolkit
portal: xyt-coach
dao_compliance: v5.0
---

# 学习力教练工具包 — SOP 分发接口 (coaching-toolkit-dispatcher)

## 一、八步 SOP 分发表 (eight-step dispatch)

触发规则：当 `eight_step_id` 匹配时，执行对应 SOP。

| eight_step_id | 步骤名 | SOP 文件 | 触发场景 |
|---|---|---|---|
| 1 | 穿透 | `coaching-sops/eight-step-sops/SOP_01-穿透.md` | 学员首次接触新知识点，stage ≤ 2 |
| 2 | 提取 | `coaching-sops/eight-step-sops/SOP_02-提取.md` | 从题目中提取关键信息结构 |
| 3 | 整理 | `coaching-sops/eight-step-sops/SOP_03-整理.md` | 知识点分类梳理，建立框架 |
| 4 | 审题 | `coaching-sops/eight-step-sops/SOP_04-审题.md` | 审题策略，stage 3-5 |
| 5 | 流程 | `coaching-sops/eight-step-sops/SOP_05-流程.md` | ★解题流程规范化(绝非"演示") |
| 6 | 批改 | `coaching-sops/eight-step-sops/SOP_06-批改.md` | 作业批改闭环，stage 4-6 |
| 7 | 分析 | `coaching-sops/eight-step-sops/SOP_07-分析.md` | 错误归因分析 |
| 8 | 估分 | `coaching-sops/eight-step-sops/SOP_08-估分.md` | 考后估分复盘，stage 5-7 |

> ⚠️ 八步第⑤步 = **流程**，绝不是"演示"。

## 二、六飞轮 SOP 分发表 (flywheel dispatch)

触发规则：当 `flywheel_id` 匹配时，执行对应飞轮 SOP。

| flywheel_id | 飞轮名 | SOP 文件 | 触发场景 |
|---|---|---|---|
| 1 | 计划飞轮 | `coaching-sops/flywheel-sops/SOP_FW1-计划飞轮.md` | 月/周/日计划制定 + 录入提醒 |
| 2 | 预习飞轮 | `coaching-sops/flywheel-sops/SOP_FW2-预习飞轮.md` | 课前预习任务分配，正确率≥40% |
| 3 | 复习飞轮 | `coaching-sops/flywheel-sops/SOP_FW3-复习飞轮.md` | 按停滞指数排序知识点，正确率≥70%晋升 |
| 4 | 听课飞轮 | `coaching-sops/flywheel-sops/SOP_FW4-听课飞轮.md` | 课前目标→课中监控→课后3句话总结 |
| 5 | 作业飞轮 | `coaching-sops/flywheel-sops/SOP_FW5-作业飞轮.md` | 布置→督促→批改→改错100%闭环 |
| 6 | 考试飞轮 | `coaching-sops/flywheel-sops/SOP_FW6-考试飞轮.md` | 考前冲刺→验收(掌握率≥80%)→考中→配合SOP_08复盘 |

> 六飞轮严格枚举：计划/预习/复习/听课/作业/考试（共6类，flywheel_id=1~6）

## 三、场景路由规则 (context routing)

```
输入: { stage: 1-7, eight_step_id?: 1-8, flywheel_id?: 1-6, scenario: string }

路由逻辑:
  IF eight_step_id → 分发到 § 一 对应 SOP
  ELIF flywheel_id → 分发到 § 二 对应 SOP
  ELIF scenario includes "计划|规划" → flywheel_id=1 (计划飞轮)
  ELIF scenario includes "预习" → flywheel_id=2
  ELIF scenario includes "复习|巩固" → flywheel_id=3
  ELIF scenario includes "听课|上课" → flywheel_id=4
  ELIF scenario includes "作业|批改" → flywheel_id=5 OR eight_step_id=6
  ELIF scenario includes "考试|估分|复盘" → flywheel_id=6 AND eight_step_id=8
  ELSE → 默认 eight_step_id=1 (穿透) 开始新知识点
```

## 四、七阶位适用范围 (stage applicability)

| 七阶 | stage值 | 优先推荐 SOP |
|---|---|---|
| 不会 | 1 | SOP_01(穿透) |
| 模糊 | 2 | SOP_01(穿透) → SOP_02(提取) |
| 清晰 | 3 | SOP_03(整理) → SOP_04(审题) |
| 框架 | 4 | SOP_04(审题) → SOP_05(流程) |
| 运用 | 5 | SOP_05(流程) → SOP_06(批改) |
| 熟练 | 6 | SOP_07(分析) → SOP_FW3(复习飞轮) |
| 创新 | 7 | SOP_08(估分) → SOP_FW6(考试飞轮) |

## 五、道层合规检查 (compliance check)

调用本 SKILL 前必须验证：

- [ ] `eight_step_id=5` 对应 SOP = **SOP_05-流程.md**（不是演示.md）
- [ ] `flywheel_id` 范围 1-6（不接受 7+）
- [ ] `stage` 范围 1-7（对应七阶：不会~创新）
- [ ] FIRE-UP 6 字母：F/I/R/E/U/P（不是5字母）
- [ ] 四密码字段：MECE(4)/JUMEQ(5)/CAMIQ(5)/FIRE-UP(6)

## 六、集成路径 (integration)

本 SKILL 从 `xingyaotu-openmaic` 主仓调用：

```
agent-skills/coach/ → Hermes Agent dispatch
  → learning-coaching-toolkit/SKILL.md (本文件)
    → coaching-sops/eight-step-sops/SOP_{01-08}.md
    → coaching-sops/flywheel-sops/SOP_FW{1-6}.md
      → assessment-toolkit SKILL.md (诊断→coaching dispatch)
```
