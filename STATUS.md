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

## 2026-05-19T00:00:00Z · Cloud Routine Phase 2 — 教练工具引擎 [开发中]

### feat(phase2): 六飞轮教练工具包引擎

| 文件 | 描述 |
|---|---|
| `src/coach/schemas.ts` | Zod schemas — StudentProfile/WeeklyPlan/SessionReport |
| `src/coach/eight-step-guide.ts` | 八步引导引擎(⑤=流程★ is_core_step=true) |
| `src/coach/flywheel-planner.ts` | 六飞轮周计划生成器(MECE 最弱维度 + 七阶推荐) |
| `src/coach/report-generator.ts` | 会话报告生成器(综合三引擎) |
| `tests/coach/*.test.ts` | 39 个测试用例 |
| `package.json` + `tsconfig.json` + `vitest.config.ts` | 项目基础设施 |
| `.github/workflows/ci.yml` | TypeCheck + Tests + 道层守护 + CSO 扫描 |

**道层合规**:
- 第5步(index=4) = 流程(★) is_core_step=true ✅
- 六飞轮 = 计划飞轮/预习飞轮/复习飞轮/听课飞轮/作业飞轮/考试飞轮 ✅
- MECE = M-动机/E-执行/C-能力/E2-环境 ✅
- 七阶 不会/模糊/清晰/框架/运用/熟练/创新 ✅

**Stage → Eight-Step(⑤=流程★)**:
- Stage 5 运用 → Step 5 流程(is_core_step=true)
- Stage 6 熟练 → Step 7 分析
- Stage 7 创新 → Step 8 估分

**CSO**: 无 API key 硬编码,无外部 API 调用 ✅

- [Next] Phase 3: 与主仓 Hermes Agent 会话集成
- [Next] Phase 2.5: 与 learning-ability-assessment-and-diagnosis 联动
