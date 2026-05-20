# 学习力教练工具包 STATUS 日志(只追加,绝不覆盖)

## 2026-05-16T07:45:00Z · Cloud Routine Phase 0 W2

- [道层 Compliance] dao-guard quick scan 0 命中 PASS
- [主仓库] xingyaotu-openmaic: Phase 0 W2 14/14 coaching_tool_catalog 已完成(PR #34)

### feat(coaching-sops): 14 SOP SKILL.md 完整套件

- [DONE] `coaching-sops/index.json` — 14 SOPs 索引(8 八步 SOP + 6 飞轮 SOP)
- [DONE] 八步 SOPs (8/8):
  - SOP_01-穿透.md | SOP_02-提取.md | SOP_03-整理.md | SOP_04-审题.md
  - SOP_05-流程.md(★第5步=流程绝非演示) | SOP_06-批改.md | SOP_07-分析.md | SOP_08-估分.md
- [DONE] 飞轮 SOPs (6/6):
  - SOP_FW1-计划飞轮.md | SOP_FW2-预习飞轮.md | SOP_FW3-复习飞轮.md
  - SOP_FW4-听课飞轮.md | SOP_FW5-作业飞轮.md | SOP_FW6-考试飞轮.md

### 道层合规汇总
- [八步] SOP_05.eight_step_name = "流程" ✅(绝不是"演示")
- [六飞轮] 无 错题/笔记/阅读/实践飞轮 ✅
- [FIRE-UP] 6 字母 F=Family/I=Individual/R=Resources/E=Ecosystem/U=Usability/P=Pathways ✅
- [七阶] 不会/模糊/清晰/框架/运用/熟练/创新 ✅

### 待办
- [x] CI workflow 配置 ← 见下方 2026-05-20 条目
- [ ] SKILL.md 与 colleague-skill 接口对接(Phase 0.5)
- [ ] 伴读标准化指导手册.docx 内容提炼入 SOPs(Phase 1)

---

## 2026-05-20T00:00:00Z · CI Workflow 配置 W1

- [触发] Cloud routine dev branch `claude/vibrant-edison-5IDBD`
- [DONE] `.github/workflows/ci.yml` — 两 Job CI 配置:
  - Job `json-validate`: python3 json.load 验证 coaching-sops/**/*.json
  - Job `dao-guard`: bash scripts/.dao-guard.sh .(v5.1 适配版)
- [DONE] `scripts/.dao-guard.sh` — v5.1 复刻
  - SCAN_DIRS: coaching-sops + docs + scripts + .github
  - 6 漂移正则全部保留,豁免 .dao-guard.sh 自身
- [道层合规] dao-guard 对空/新目录 → PASS;6 漂移项检测覆盖 coaching-sops 全部 MD+JSON
- [Next] SKILL.md 与 colleague-skill 接口对接(Phase 0.5)

---
