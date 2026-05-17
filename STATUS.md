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
- [六飞轮] 六飞轮 = 计划/预习/复习/听课/作业/考试(严格枚举) ✅
- [FIRE-UP] 6 字母 F=Family/I=Individual/R=Resources/E=Ecosystem/U=Usability/P=Pathways ✅
- [七阶] 不会/模糊/清晰/框架/运用/熟练/创新 ✅

### 待办
- [x] CI workflow 配置 ← 已完成(见下)
- [ ] SKILL.md 与 colleague-skill 接口对接(Phase 0.5)
- [ ] 伴读标准化指导手册.docx 内容提炼入 SOPs(Phase 1)

---

## 2026-05-17T13:25Z · CI 配置完成(Cloud Routine 自跑)

[Done] `scripts/.dao-guard.sh` v5.1 — 道层零漂移守护脚本新增(与主仓 xingyaotu-openmaic 同步)
[Done] `.github/workflows/dao-guard-ci.yml` — 完整 CI workflow 新增,使用 .dao-guard.sh 脚本
       (补充原有 validate.yml 中的 inline 简化检查)
[Next] SKILL.md 与 colleague-skill 接口对接(Phase 0.5)
[Next] 伴读标准化指导手册.docx 内容提炼入 SOPs(Phase 1)

---

## 2026-05-17T13:45Z · 道层守护 CI 修复(Cloud Routine 自跑)

[Done] 修复 SOP 合规说明中的漂移关键词字面量(第六轮 CI 修复):
  - `SOP_05-流程.md` 合规注: 删除禁用飞轮名称字面量,改为枚举式
  - `SOP_FW3-复习飞轮.md` 合规注: 删除禁用飞轮名称字面量
  - `SOP_FW5-作业飞轮.md` 合规注: 删除禁用飞轮名称字面量
  - `SOP_01-穿透.md` 合规注: 删除禁用飞轮名称字面量
  - `SOP_02-提取.md` 合规注: 删除禁用飞轮名称字面量
  - `STATUS.md` 合规汇总: 删除 实践飞轮 字面量,改为枚举式
[Note] 根本原因: 合规说明常用"无 X"或“不得使用 X”类错误表述,导致 X 字面出现并触发模式
       正确写法: 改用枚举合法元素(计划/预习/复习/听课/作业/考试),不赞载字面量
[Next] SKILL.md 与 colleague-skill 接口对接(Phase 0.5)
[Next] 伴读标准化指导手册.docx 内容提炼入 SOPs(Phase 1)

---
