import { describe, it, expect } from "vitest";
import { generateSessionReport } from "../../src/coach/report-generator";
import type { CoachingSessionInput } from "../../src/coach/schemas";

const sampleInput: CoachingSessionInput = {
  session_id: "sess_20260519_001",
  student: {
    student_id: "stu_001",
    grade: "高二",
    subject: "物理",
    mece_scores: { M: 60, E: 45, C: 75, E2: 55 },
    current_stage_id: 4,
    current_flywheel_id: 4,
  },
  session_notes: "今天重点练习受力分析的框架搭建",
  session_date: "2026-05-19",
};

describe("generateSessionReport — 会话报告", () => {
  it("session_id 正确", () => {
    const report = generateSessionReport(sampleInput);
    expect(report.session_id).toBe("sess_20260519_001");
  });

  it("student_id 正确", () => {
    expect(generateSessionReport(sampleInput).student_id).toBe("stu_001");
  });

  it("stage 4 → stage_name=框架", () => {
    const report = generateSessionReport(sampleInput);
    expect(report.current_stage_id).toBe(4);
    expect(report.current_stage_name_zh).toBe("框架");
  });

  it("MECE weakest = E (45 最低)", () => {
    const report = generateSessionReport(sampleInput);
    expect(report.mece_summary.weakest_dimension).toBe("E");
    expect(report.mece_summary.weakest_label_zh).toBe("执行");
  });

  it("stage 4 → eight_step=审题 (step 4)", () => {
    const report = generateSessionReport(sampleInput);
    expect(report.eight_step_guidance.step_id).toBe(4);
    expect(report.eight_step_guidance.step_name).toBe("审题");
    expect(report.eight_step_guidance.is_core_step).toBe(false);
  });

  it("stage 5 → eight_step=流程, is_core_step=true ★", () => {
    const i5: CoachingSessionInput = {
      ...sampleInput,
      student: { ...sampleInput.student, current_stage_id: 5, current_flywheel_id: 5 },
    };
    const report = generateSessionReport(i5);
    expect(report.eight_step_guidance.step_name).toBe("流程");
    expect(report.eight_step_guidance.is_core_step).toBe(true);
  });

  it("weekly_plan 存在且有 items", () => {
    const report = generateSessionReport(sampleInput);
    expect(report.weekly_plan.items.length).toBeGreaterThan(0);
  });

  it("generated_at 为 ISO datetime", () => {
    const report = generateSessionReport(sampleInput);
    expect(() => new Date(report.generated_at).toISOString()).not.toThrow();
  });

  it("mece_summary 四维数值正确", () => {
    const report = generateSessionReport(sampleInput);
    expect(report.mece_summary.M).toBe(60);
    expect(report.mece_summary.E).toBe(45);
    expect(report.mece_summary.C).toBe(75);
    expect(report.mece_summary.E2).toBe(55);
  });

  it("session_date 保留", () => {
    const report = generateSessionReport(sampleInput);
    expect(report.session_date).toBe("2026-05-19");
  });
});
