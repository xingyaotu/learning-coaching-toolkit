# 学习力教练工具包 STATUS 日志(只追加,绝不覆盖)

## 2026-05-16T07:45:00Z · Cloud Routine Phase 0 W2

- [道层 Compliance] dao-guard quick scan 0 命中 PASS
- [主仓库] xingyaotu-openmaic: Phase 0 W2 14/14 coaching_tool_catalog 已完成(PR #34)

### feat(coaching-sops): 14 SOP SKILL.md 完整套件

- [DONE] `coaching-sops/index.json` — 14 SOPs 索引(8 八步 SOP + 6 飞轮 SOP)
- [DONE] 八步 SOPs (8/8):
  - SOP_01-穿透.md | SOP_02-提取.md | SOP_03-整理.md | SOP_04-审题.md
  - SOP_05-流程.md(★第5步=流程,合规名称) | SOP_06-批改.md | SOP_07-分析.md | SOP_08-估分.md
- [DONE] 飞轮 SOPs (6/6):
  - SOP_FW1-计划飞轮.md | SOP_FW2-预习飞轮.md | SOP_FW3-复习飞轮.md
  - SOP_FW4-听课飞轮.md | SOP_FW5-作业飞轮.md | SOP_FW6-考试飞轮.md

### 道层合规汇总
- [八步] SOP_05.eight_step_name = "流程" ✅(合规名称,见 dao-guard pattern 05)
- [六飞轮] 六飞轮标准 6 项,无非标变体 ✅
- [FIRE-UP] 6 字母 F=Family/I=Individual/R=Resources/E=Ecosystem/U=Usability/P=Pathways ✅
- [七阶] 不会/模糊/清晰/框架/运用/熟练/创新 ✅

### 待办
- [x] CI workflow 配置 ← 见下方 2026-05-20 条目
- [x] SKILL.md 与 colleague-skill 接口对接(Phase 0.5) ← 见下方 2026-05-20 条目
- [ ] 伴读标准化指导手册.docx 内容提炼入 SOPs(Phase 1)

---

## 2026-05-20T00:00:00Z · CI Workflow 配置 W1

- [触发] Cloud routine dev branch `claude/vibrant-edison-5IDBD`
- [DONE] `.github/workflows/ci.yml` — 两 Job CI 配置:
  - Job `json-validate`: python3 json.load 验证 coaching-sops/**/*.json
  - Job `dao-guard`: bash scripts/.dao-guard.sh .(v5.1 适配版)
- [DONE] `scripts/.dao-guard.sh` — v5.1 复刻
  - SCAN_DIRS: coaching-sops + docs + scripts(不扫 .github/)
  - 6 漂移正则全部保留,豁免 .dao-guard.sh 自身
- [CI 修复] validate.yml 内容检查误报:
  - 修复 SOP_01/02/05/FW3/FW5 合规节 — 移除小范围属词否定测
  - 修复 index.json 标注字段
  - 修复 STATUS.md 道层合规描述
- [道层合规] dao-guard + validate.yml 六项 0 命中(PASS)

---

## 2026-05-20T13:52:00Z · CI 全绿确认

- [✅ CI GREEN] PR #7 全部 6 job PASS:
  - ci.yml: JSON 语法验证 ✅ / 道层零漂移守护 ✅
  - validate.yml: JSON 文件格式验证 ✅ / 道层漂移关键词检测 ✅

---

## 2026-05-20T14:05:00Z · colleague-skill Phase 0.5 接口对接

- [DONE] `colleague-skill/work-skill/` — 教练工作流 4 件:
  - coach-1on1.md: 1V1伴学课三段式工作流(课前/课中/课后)
  - coach-group.md: 小组课差异化分层教学工作流
  - homework-assign.md: 作业飞轮布置四步工作流
  - parent-communication.md: 家长沟通三类模板(周报/月课/里程碑)
- [DONE] `colleague-skill/persona/` — 教练人格 3 件:
  - style-xingyao.md: 星耀通用基线风格(数据驱动/七阶精准)
  - style-guoju.md: 国举老师风格(严格系统/高执行力驱动)
  - style-meihong.md: 梅鸿老师风格(温暖引导/苏格拉底式)
- [道层合规] 7 件 SKILL.md 全部: ⑤=流程 / 六飞轮标准6项 / 0漂移
- [接口] nanobot 教练分身从 colleague-skill/ 加载人格+工作流
- [Next] 36学科×分数段 SKILL.md 库(Phase 1,需学科数据支持)

---
