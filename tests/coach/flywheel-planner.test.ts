import { describe, it, expect } from "vitest";
import { generateWeeklyPlan } from "../../src/coach/flywheel-planner";
import type { StudentProfile } from "../../src/coach/schemas";

const baseStudent: StudentProfile = {
  student_id: "stu_001",
  grade: "高一",
  subject: "数学",
  mece_scores: { M: 50, E: 40, C: 70, E2: 60 },
  current_stage_id: 3,
  current_flywheel_id: 3,
};

describe("generateWeeklyPlan — 六飞轮周计划", () => {
  it("返回合法结构", () => {
    const plan = generateWeeklyPlan(baseStudent, "2026-05-19");
    expect(plan.student_id).toBe("stu_001");
    expect(plan.items.length).toBeGreaterThanOrEqual(1);
    expect(plan.total_minutes).toBeGreaterThan(0);
  });

  it("焦点维度 = MECE 最弱维度 (E=40 最低)", () => {
    const plan = generateWeeklyPlan(baseStudent, "2026-05-19");
    expect(plan.focus_dimension).toBe("E");
    expect(plan.focus_label_zh).toBe("执行");
  });

  it("目标阶段 = 当前阶段+1", () => {
    const plan = generateWeeklyPlan(baseStudent, "2026-05-19");
    expect(plan.target_stage_id).toBe(4);
  });

  it("stage 5 运用的首要任务 → 八步⑤=流程 ★", () => {
    const student5: StudentProfile = {
      ...baseStudent,
      current_stage_id: 5,
      current_flywheel_id: 5,
    };
    const plan = generateWeeklyPlan(student5, "2026-05-19");
    const primary = plan.items[0];
    expect(primary.eight_step_id).toBe(5);
    expect(primary.eight_step_name).toBe("流程");
  });

  it("stage 7 目标阶段钳制在 7", () => {
    const s7: StudentProfile = {
      ...baseStudent,
      current_stage_id: 7,
      current_flywheel_id: 6,
    };
    expect(generateWeeklyPlan(s7, "2026-05-19").target_stage_id).toBe(7);
  });

  it("items 优先级为 high/medium/low", () => {
    const plan = generateWeeklyPlan(baseStudent, "2026-05-19");
    for (const item of plan.items) {
      expect(["high", "medium", "low"]).toContain(item.priority);
    }
  });

  it("estimated_minutes 在 10-120 之间", () => {
    const plan = generateWeeklyPlan(baseStudent, "2026-05-19");
    for (const item of plan.items) {
      expect(item.estimated_minutes).toBeGreaterThanOrEqual(10);
      expect(item.estimated_minutes).toBeLessThanOrEqual(120);
    }
  });

  it("total_minutes = items 之和", () => {
    const plan = generateWeeklyPlan(baseStudent, "2026-05-19");
    const sum = plan.items.reduce((acc, i) => acc + i.estimated_minutes, 0);
    expect(plan.total_minutes).toBe(sum);
  });

  it("E2 最弱 → focus=E2/环境", () => {
    const s: StudentProfile = {
      ...baseStudent,
      mece_scores: { M: 80, E: 80, C: 80, E2: 20 },
    };
    const plan = generateWeeklyPlan(s, "2026-05-19");
    expect(plan.focus_dimension).toBe("E2");
    expect(plan.focus_label_zh).toBe("环境");
  });
});
