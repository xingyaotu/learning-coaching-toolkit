import { EIGHT_STEP_NAMES, SIX_FLYWHEEL_NAMES, MECE_LABELS, MECE_DIMENSION_KEYS } from "./schemas";
import type { StudentProfile, WeeklyPlan, WeeklyPlanItem, MeceDimensionKey } from "./schemas";

const STAGE_EIGHT_STEP_MAP: [number, number, number, number, number, number, number] =
  [1, 2, 3, 4, 5, 7, 8];

const STAGE_FLYWHEEL_MAP: [number, number, number, number, number, number, number] =
  [1, 2, 3, 4, 5, 6, 1];

const FLYWHEEL_BASE_MINUTES: Record<number, number> = {
  1: 30,
  2: 45,
  3: 60,
  4: 45,
  5: 60,
  6: 90,
};

function getWeakestDimension(scores: Record<MeceDimensionKey, number>): MeceDimensionKey {
  const entries = MECE_DIMENSION_KEYS.map((k) => [k, scores[k]] as [MeceDimensionKey, number]);
  return entries.reduce((weakest, current) =>
    current[1] < weakest[1] ? current : weakest
  )[0];
}

export function generateWeeklyPlan(student: StudentProfile, weekStart: string): WeeklyPlan {
  const stageId = student.current_stage_id;
  const targetStageId = Math.min(7, stageId + 1) as 1 | 2 | 3 | 4 | 5 | 6 | 7;
  const weakestDim = getWeakestDimension(student.mece_scores);

  const eightStepId = STAGE_EIGHT_STEP_MAP[stageId - 1];
  const flywheelId = STAGE_FLYWHEEL_MAP[stageId - 1];

  const primaryItem: WeeklyPlanItem = {
    flywheel_id: flywheelId,
    flywheel_name: SIX_FLYWHEEL_NAMES[flywheelId - 1],
    eight_step_id: eightStepId,
    eight_step_name: EIGHT_STEP_NAMES[eightStepId - 1],
    priority: "high",
    action_zh: `${SIX_FLYWHEEL_NAMES[flywheelId - 1]}强化: ${EIGHT_STEP_NAMES[eightStepId - 1]}练习`,
    estimated_minutes: FLYWHEEL_BASE_MINUTES[flywheelId],
  };

  const items: WeeklyPlanItem[] = [primaryItem];

  if (targetStageId > stageId) {
    const targetFlywheelId = STAGE_FLYWHEEL_MAP[targetStageId - 1];
    const targetEightStepId = STAGE_EIGHT_STEP_MAP[targetStageId - 1];
    if (targetFlywheelId !== flywheelId) {
      items.push({
        flywheel_id: targetFlywheelId,
        flywheel_name: SIX_FLYWHEEL_NAMES[targetFlywheelId - 1],
        eight_step_id: targetEightStepId,
        eight_step_name: EIGHT_STEP_NAMES[targetEightStepId - 1],
        priority: "medium",
        action_zh: `${SIX_FLYWHEEL_NAMES[targetFlywheelId - 1]}预备: ${EIGHT_STEP_NAMES[targetEightStepId - 1]}入门`,
        estimated_minutes: Math.min(60, FLYWHEEL_BASE_MINUTES[targetFlywheelId]),
      });
    }
  }

  const totalMinutes = items.reduce((sum, item) => sum + item.estimated_minutes, 0);

  return {
    student_id: student.student_id,
    week_start: weekStart,
    focus_dimension: weakestDim,
    focus_label_zh: MECE_LABELS[weakestDim],
    target_stage_id: targetStageId,
    items,
    total_minutes: totalMinutes,
  };
}
