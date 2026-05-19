import { z } from "zod";

export const MASTERY_STAGE_NAMES = [
  "不会",
  "模糊",
  "清晰",
  "框架",
  "运用",
  "熟练",
  "创新",
] as const;

export const EIGHT_STEP_NAMES = [
  "穿透",
  "提取",
  "整理",
  "审题",
  "流程",
  "批改",
  "分析",
  "估分",
] as const;

export const SIX_FLYWHEEL_NAMES = [
  "计划飞轮",
  "预习飞轮",
  "复习飞轮",
  "听课飞轮",
  "作业飞轮",
  "考试飞轮",
] as const;

export const MECE_DIMENSION_KEYS = ["M", "E", "C", "E2"] as const;
export type MeceDimensionKey = (typeof MECE_DIMENSION_KEYS)[number];

export const MECE_LABELS: Record<MeceDimensionKey, string> = {
  M: "动机",
  E: "执行",
  C: "能力",
  E2: "环境",
};

export const StageIdSchema = z.number().int().min(1).max(7);
export const EightStepIdSchema = z.number().int().min(1).max(8);
export const FlywheelIdSchema = z.number().int().min(1).max(6);

export const MeceScoreMapSchema = z.object({
  M: z.number().min(0).max(100),
  E: z.number().min(0).max(100),
  C: z.number().min(0).max(100),
  E2: z.number().min(0).max(100),
});
export type MeceScoreMap = z.infer<typeof MeceScoreMapSchema>;

export const StudentProfileSchema = z.object({
  student_id: z.string().min(1),
  grade: z.string().min(1),
  subject: z.string().min(1),
  mece_scores: MeceScoreMapSchema,
  current_stage_id: StageIdSchema,
  current_flywheel_id: FlywheelIdSchema,
});
export type StudentProfile = z.infer<typeof StudentProfileSchema>;

export const CoachingSessionInputSchema = z.object({
  session_id: z.string().min(1),
  student: StudentProfileSchema,
  session_notes: z.string().max(2000),
  session_date: z.string().min(1),
});
export type CoachingSessionInput = z.infer<typeof CoachingSessionInputSchema>;

export const WeeklyPlanItemSchema = z.object({
  flywheel_id: FlywheelIdSchema,
  flywheel_name: z.enum(SIX_FLYWHEEL_NAMES),
  eight_step_id: EightStepIdSchema,
  eight_step_name: z.enum(EIGHT_STEP_NAMES),
  priority: z.enum(["high", "medium", "low"]),
  action_zh: z.string().min(1),
  estimated_minutes: z.number().int().min(10).max(120),
});
export type WeeklyPlanItem = z.infer<typeof WeeklyPlanItemSchema>;

export const WeeklyPlanSchema = z.object({
  student_id: z.string(),
  week_start: z.string(),
  focus_dimension: z.enum(MECE_DIMENSION_KEYS),
  focus_label_zh: z.string(),
  target_stage_id: StageIdSchema,
  items: z.array(WeeklyPlanItemSchema).min(1).max(6),
  total_minutes: z.number().int(),
});
export type WeeklyPlan = z.infer<typeof WeeklyPlanSchema>;

export const SessionReportSchema = z.object({
  session_id: z.string(),
  student_id: z.string(),
  session_date: z.string(),
  current_stage_id: StageIdSchema,
  current_stage_name_zh: z.enum(MASTERY_STAGE_NAMES),
  mece_summary: z.object({
    M: z.number().min(0).max(100),
    E: z.number().min(0).max(100),
    C: z.number().min(0).max(100),
    E2: z.number().min(0).max(100),
    weakest_dimension: z.enum(MECE_DIMENSION_KEYS),
    weakest_label_zh: z.string(),
  }),
  weekly_plan: WeeklyPlanSchema,
  eight_step_guidance: z.object({
    step_id: EightStepIdSchema,
    step_name: z.enum(EIGHT_STEP_NAMES),
    guidance_zh: z.string(),
    is_core_step: z.boolean(),
  }),
  generated_at: z.string(),
});
export type SessionReport = z.infer<typeof SessionReportSchema>;
