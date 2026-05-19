import { generateWeeklyPlan } from "./flywheel-planner";
import { getStepForStage } from "./eight-step-guide";
import { MASTERY_STAGE_NAMES, MECE_LABELS, MECE_DIMENSION_KEYS } from "./schemas";
import type { CoachingSessionInput, SessionReport, MeceDimensionKey } from "./schemas";

function getWeakestDimension(
  scores: Record<MeceDimensionKey, number>
): MeceDimensionKey {
  const entries = MECE_DIMENSION_KEYS.map((k) => [k, scores[k]] as [MeceDimensionKey, number]);
  return entries.reduce((weakest, current) =>
    current[1] < weakest[1] ? current : weakest
  )[0];
}

export function generateSessionReport(input: CoachingSessionInput): SessionReport {
  const { session_id, student, session_date } = input;
  const stageIdx = student.current_stage_id - 1;

  const weeklyPlan = generateWeeklyPlan(student, session_date);
  const stepGuidance = getStepForStage(student.current_stage_id);
  const weakestDim = getWeakestDimension(student.mece_scores);

  return {
    session_id,
    student_id: student.student_id,
    session_date,
    current_stage_id: student.current_stage_id,
    current_stage_name_zh: MASTERY_STAGE_NAMES[stageIdx],
    mece_summary: {
      M: student.mece_scores.M,
      E: student.mece_scores.E,
      C: student.mece_scores.C,
      E2: student.mece_scores.E2,
      weakest_dimension: weakestDim,
      weakest_label_zh: MECE_LABELS[weakestDim],
    },
    weekly_plan: weeklyPlan,
    eight_step_guidance: {
      step_id: stepGuidance.step_id,
      step_name: stepGuidance.step_name,
      guidance_zh: stepGuidance.guidance_zh,
      is_core_step: stepGuidance.is_core_step,
    },
    generated_at: new Date().toISOString(),
  };
}
