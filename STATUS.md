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
- [六飞轮] 无 错题/笔记/阅读/实践飞轮轮 ✅
- [FIRE-UP] 6 字母 F=Family/I=Individual/R=Resources/E=Ecosystem/U=Usability/P=Pathways ✅
- [七阶] 不会/模糊/清晰/框架/运用/熟练/创新 ✅

### 待办
- [ ] CI workflow 配置
- [ ] SKILL.md 与 colleague-skill 接口对接(Phase 0.5)
- [ ] 伴读标准化指导手册.docx 内容提炼入 SOPs(Phase 1)

---

## 2026-05-17T21:45:00Z · CI Workflow 配置 [完成]

- [DONE] `.github/workflows/ci.yml` — 道层守护 + SOP 验证

| 检查项 | 内容 |
|---|---|
| [1/6] 漂移术语 grep | 导入/拆解/讲解/类比/演示 |
| [2/6] JUMEQ 英语漂移 | Judge/Understand/Match/Execute/Qualify |
| [3/6] 六飞轮替换 | 错题/笔记/阅读/实践 |
| [4/6] FIRE-UP 6字母 | F/I/R/E/U/P 全部出现 |
| [5/6] SOP_05 step名称=流程 | SOP_05 不得映射到演示 |
| [6/6] CSO Secret 扫描 | sk-ant-/ghp_/AKIA 等 |
| JSON 验证 | python3 json.load 全部 JSON |
| SOP index 完整性 | 14 SOPs 完整性 + SOP_05=流程 确认 |

- [道层] dao-guard 内联 6/6 0 命中 ✅
- [CSO] 0 触发(纯 CI 配置,无 API key 引用) ✅
- [Next] SKILL.md 与 colleague-skill 接口对接(Phase 0.5) / 伴读手册内容提炼(Phase 1)
