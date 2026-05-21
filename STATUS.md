# 学习力教练工具包 STATUS 日志(只追加,绝不覆盖)

## 2026-05-16T07:45:00Z · Cloud Routine Phase 0 W2

- [道层 Compliance] dao-guard quick scan 0 命中 PASS
- [主仓库] xingyaotu-openmaic: Phase 0 W2 14/14 coaching_tool_catalog 已完成(PR #34)

### feat(coaching-sops): 14 SOP SKILL.md 完整套件

- [DONE] `coaching-sops/index.json` — 14 SOPs 索引(8 八步 SOP + 6 飞轮 SOP)
- [DONE] 八步 SOPs (8/8):
  - SOP_01-穿透.md | SOP_02-提取.md | SOP_03-整理.md | SOP_04-审题.md
  - SOP_05-流程.md(★第5步=流程 ✅) | SOP_06-批改.md | SOP_07-分析.md | SOP_08-估分.md
- [DONE] 飞轮 SOPs (6/6):
  - SOP_FW1-计划飞轮.md | SOP_FW2-预习飞轮.md | SOP_FW3-复习飞轮.md
  - SOP_FW4-听课飞轮.md | SOP_FW5-作业飞轮.md | SOP_FW6-考试飞轮.md

### 道层合规汇总
- [八步] SOP_05.eight_step_name = "流程" ✅ 合规已验证
- [六飞轮] 六飞轮名称合规(无非法变体) ✅
- [FIRE-UP] 6 字母 F=Family/I=Individual/R=Resources/E=Ecosystem/U=Usability/P=Pathways ✅
- [七阶] 不会/模糊/清晰/框架/运用/熟练/创新 ✅

### 待办
- [ ] CI workflow 配置
- [ ] SKILL.md 与 colleague-skill 接口对接(Phase 0.5)
- [ ] 伴读标准化指导手册.docx 内容提炼入 SOPs(Phase 1)

---

---

## 2026-05-20T17:22:00Z · coaching-toolkit — SOP 完整性验证脚本

### feat(scripts+ci): validate-sop-completeness.py — 14 SOP 文件完整性道层验证

- `scripts/validate-sop-completeness.py`: 14 SOP 完整性验证脚本
  - 八步 SOP 8/8: SOP_01~SOP_08 文件存在性
  - ⑤守护: SOP_05-流程.md 存在，漂移文件名不存在
  - 六飞轮 SOP 6/6: SOP_FW1~SOP_FW6 文件存在性
  - index.json 条目: 14/14 (八步8 + 飞轮6) + SOP_05.name_zh='流程'
- `.github/workflows/validate.yml`: 新增 `sop-completeness` CI job
- 本地验证: 20/20 通过 ✅

- [道层] SOP 完整性全部通过 ✅ | CSO 0触发 ✅
- [Next] coaching-toolkit → 继续推进其他待办任务

---

## 2026-05-20T17:50:00Z · coaching-toolkit — SOP SKILL 目录接口

### feat(pipeline-data): sop-skill-catalog.json — 14 SOP colleague-skill 接口目录

- `pipeline-data/sop-skill-catalog.json`: 14 SOP 的 colleague-skill 接口目录
  - 全部 14 条: $schema + 8 八步 SOP + 6 飞轮 SOP
  - 每条含: sop_id / name / description / use_when / stage_range / allowed_tools / file
  - ⑤守护: SOP_05.eight_step_name = "流程" ✅, ★_note 无漂移字面量
  - 六飞轮: six_flywheel_name 全用单词(计划/预习/复习/听课/作业/考试)
- 道层漂移: 0 命中 ✅ | JSON 格式: 有效 ✅

### [Next] coaching-toolkit
- [x] validate-sop-completeness.py 扩展: 校验 sop-skill-catalog.json 条目与 SOP 文件一致性 ✅
- [ ] colleague-skill 正式接口对接(Phase 0.5)

---

## 2026-05-21T00:00:00Z · coaching-toolkit — validate-sop-completeness.py v1.1 交叉验证

### feat(scripts): validate-sop-completeness.py v1.1 — sop-skill-catalog.json 交叉验证

- `scripts/validate-sop-completeness.py` 升级 v1.0 → v1.1
  - [5] 新增 `validate_sop_skill_catalog()` — sop-skill-catalog.json 交叉验证
    - $schema 字段存在性
    - 条目总数 14/14 (八步8 + 飞轮6)
    - catalog → 文件: 14/14 file 路径存在
    - SOP_05.eight_step_name='流程' + eight_step_id=5 ⑤守护
    - 六飞轮 name 枚举守护 (合规/非法变体检测)
    - 文件 → catalog 反向检查: 14/14 每个 SOP 文件有对应条目
  - 本地验证: 54/54 通过 ✅

- [道层] 0 触发 ✅ | JSON 格式: 有效 ✅
- [Next] colleague-skill 正式接口对接(Phase 0.5)

---

## 2026-05-21T04:15:00Z · coaching-toolkit — Phase 0.5 colleague-skill 接口

### feat(colleague-skills): 14 SOP SKILL.md 接口目录 — Phase 0.5

- `scripts/generate-colleague-skills.py`: 从 sop-skill-catalog.json 生成 14 SKILL.md
- `colleague-skills/eight-step-sops/`: 8 个八步 SOP SKILL.md (sop-01 ~ sop-08)
- `colleague-skills/flywheel-sops/`: 6 个飞轮 SOP SKILL.md (sop-fw1 ~ sop-fw6)
  - 每个 SKILL.md 含: name/description/version/allowed-tools/portal/quadruple_context
  - sop-05.skill.md: eight_step_id=5, eight_step_name=流程 ★_note=合规 ✅
  - 六飞轮: 计划/预习/复习/听课/作业/考试(全枚举合规)

- [道层] 内容检查 3 项全 0 命中 ✅ | JSON 格式: 有效 ✅ | SOP 完整性 54/54 ✅
- [Next] colleague-skill 正式注册接口对接(Phase 1) | IRT 参数标定(Phase 2.5)

---

## 2026-05-21T04:25:00Z · coaching-toolkit — colleague-skill 验证脚本

### feat(scripts+ci): validate-colleague-skills.py — SKILL.md frontmatter 合规验证

- `scripts/validate-colleague-skills.py`: 14 SKILL.md frontmatter 验证
  - 目录结构: eight-step-sops/ + flywheel-sops/ ✓
  - 八步 × 8: frontmatter 字段完整 + portal 合规 ✓
  - SOP_05 ⑤守护: eight_step_id=5 + eight_step_name='流程' ✓
  - 飞轮 × 6: frontmatter 字段完整 + portal 合规 ✓
  - 六飞轮名称守护: 计划/预习/复习/听课/作业/考试 全枚举 ✓
  - SKILL.md 总数 14/14 ✓
- `.github/workflows/validate.yml`: 升级 v5.0→v5.1, 新增 `colleague-skills` CI job
- 本地验证: 全部通过 ✅

- [道层] 0触发 ✅ | [Next] colleague-skill Phase 1 正式注册接口
