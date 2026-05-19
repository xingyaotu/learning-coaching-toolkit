import { describe, it, expect } from "vitest";
import { getEightStepGuidance, getStepForStage } from "../../src/coach/eight-step-guide";

describe("getEightStepGuidance — 八步引导", () => {
  it("步骤1 = 穿透, is_core_step=false", () => {
    const g = getEightStepGuidance(1);
    expect(g.step_name).toBe("穿透");
    expect(g.is_core_step).toBe(false);
    expect(g.guidance_zh).toBeTruthy();
  });

  it("步骤5 = 流程, is_core_step=true ★", () => {
    const g = getEightStepGuidance(5);
    expect(g.step_id).toBe(5);
    expect(g.step_name).toBe("流程");
    expect(g.is_core_step).toBe(true);
  });

  it("步骤5 guidance 不含演示/拆解/讲解", () => {
    const g = getEightStepGuidance(5);
    expect(g.guidance_zh).not.toContain("演示");
    expect(g.guidance_zh).not.toContain("拆解");
    expect(g.guidance_zh).not.toContain("讲解");
  });

  it("步骤8 = 估分", () => {
    const g = getEightStepGuidance(8);
    expect(g.step_name).toBe("估分");
    expect(g.is_core_step).toBe(false);
  });

  it("所有步骤均有 guidance_zh", () => {
    for (let i = 1; i <= 8; i++) {
      const g = getEightStepGuidance(i);
      expect(g.guidance_zh.length).toBeGreaterThan(5);
    }
  });

  it("越界 step 0 抛错", () => {
    expect(() => getEightStepGuidance(0)).toThrow();
  });

  it("越界 step 9 抛错", () => {
    expect(() => getEightStepGuidance(9)).toThrow();
  });
});

describe("getStepForStage — 阶段→步骤", () => {
  it("stage 1 → 步骤1 穿透", () => {
    expect(getStepForStage(1).step_name).toBe("穿透");
  });

  it("stage 5 → 步骤5 流程 ★", () => {
    const g = getStepForStage(5);
    expect(g.step_name).toBe("流程");
    expect(g.is_core_step).toBe(true);
  });

  it("stage 6 → 步骤7 分析", () => {
    expect(getStepForStage(6).step_name).toBe("分析");
  });

  it("stage 7 → 步骤8 估分", () => {
    expect(getStepForStage(7).step_name).toBe("估分");
  });

  it("越界 stage 0 抛错", () => {
    expect(() => getStepForStage(0)).toThrow();
  });

  it("越界 stage 8 抛错", () => {
    expect(() => getStepForStage(8)).toThrow();
  });
});
