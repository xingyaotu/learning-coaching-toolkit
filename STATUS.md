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
- [ ] CI workflow 配置
- [ ] SKILL.md 与 colleague-skill 接口对接(Phase 0.5)
- [ ] 伴读标准化指导手册.docx 内容提炼入 SOPs(Phase 1)

---

## 2026-05-18T03:55Z · SKILL.md colleague-skill 接口上线 (Cloud Routine 自跑)

[Done] CI workflow — `validate.yml` 已在前次 PR 完成 ✅(非本次新增)

[Done] feat(skill-interface): SKILL.md 教练工具包 SOP 分发接口

- 八步 SOP 分发表(eight_step_id 1-8 → SOP 文件完整映射)
- 六飞轮 SOP 分发表(flywheel_id 1-6 → SOP 文件完整映射)
- 场景路由规则(context routing: 关键词 → flywheel/eight_step 自动选择)
- 七阶位适用范围(stage 1-7 → 优先推荐 SOP)
- 道层合规检查项(调用前验证清单)
- 集成路径(openmaic agent-skills → coaching-toolkit → assessment-toolkit)

[道层] 漂移词 0 命中 ✅ | 八步⑤=流程 ✅ | 六飞轮 1-6 严格 ✅

[Next] 伴读标准化指导手册.docx 内容提炼入 SOPs(Phase 1) — 待人工上传 docx 内容
[Next] assessment-toolkit SKILL.md 接口对接(镜像本 PR 工作到 assessment 仓)

