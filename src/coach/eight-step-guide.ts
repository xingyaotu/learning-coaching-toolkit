import { EIGHT_STEP_NAMES } from "./schemas";

const EIGHT_STEP_GUIDANCE: Record<number, string> = {
  1: "穿透核心: 找出题目最底层的知识点和认知盲区，精准定位问题本质",
  2: "提取要素: 从题干中提取已知条件、未知量和隐含条件，建立信息清单",
  3: "整理框架: 将提取的信息按知识体系归类整理，画出知识关联图",
  4: "审题技巧: 识别题型特征和解题路径，选择最优解题思路",
  5: "流程规范: 按标准解题流程逐步推导，确保每步有理有据，形成规范化解题习惯",
  6: "批改对标: 对照标准答案逐步核查，定位失分点，分析错误类型",
  7: "深度分析: 分析错误根因(动机/执行/能力/环境四维度)，提炼可迁移规律",
  8: "科学估分: 基于得分规律和题型难度建立估分模型，提升元认知能力",
};

const IS_CORE_STEP: Record<number, boolean> = {
  1: false,
  2: false,
  3: false,
  4: false,
  5: true,
  6: false,
  7: false,
  8: false,
};

export interface EightStepGuidance {
  step_id: number;
  step_name: string;
  guidance_zh: string;
  is_core_step: boolean;
}

export function getEightStepGuidance(stepId: number): EightStepGuidance {
  if (stepId < 1 || stepId > 8) {
    throw new Error(`步骤ID必须在1-8之间，当前: ${stepId}`);
  }
  return {
    step_id: stepId,
    step_name: EIGHT_STEP_NAMES[stepId - 1],
    guidance_zh: EIGHT_STEP_GUIDANCE[stepId],
    is_core_step: IS_CORE_STEP[stepId],
  };
}

const STAGE_STEP_MAP: [number, number, number, number, number, number, number] =
  [1, 2, 3, 4, 5, 7, 8];

export function getStepForStage(stageId: number): EightStepGuidance {
  if (stageId < 1 || stageId > 7) {
    throw new Error(`阶段ID必须在1-7之间，当前: ${stageId}`);
  }
  const stepId = STAGE_STEP_MAP[stageId - 1];
  return getEightStepGuidance(stepId);
}
