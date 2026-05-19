import { describe, it, expect } from "vitest";
import {
  EIGHT_STEP_NAMES,
  SIX_FLYWHEEL_NAMES,
  MASTERY_STAGE_NAMES,
  MECE_LABELS,
} from "../../src/coach/schemas";

describe("道层守护 — 教练工具包基准", () => {
  it("八步共 8 个", () => {
    expect(EIGHT_STEP_NAMES).toHaveLength(8);
  });

  it("第1步=穿透", () => {
    expect(EIGHT_STEP_NAMES[0]).toBe("穿透");
  });

  it("第5步(index 4)=流程 ★", () => {
    expect(EIGHT_STEP_NAMES[4]).toBe("流程");
  });

  it("第5步非演示/拆解/讲解/类比", () => {
    expect(EIGHT_STEP_NAMES[4]).not.toBe("演示");
    expect(EIGHT_STEP_NAMES[4]).not.toBe("拆解");
    expect(EIGHT_STEP_NAMES[4]).not.toBe("讲解");
    expect(EIGHT_STEP_NAMES[4]).not.toBe("类比");
  });

  it("第8步=估分", () => {
    expect(EIGHT_STEP_NAMES[7]).toBe("估分");
  });

  it("六飞轮共 6 个", () => {
    expect(SIX_FLYWHEEL_NAMES).toHaveLength(6);
  });

  it("六飞轮第1=计划飞轮", () => {
    expect(SIX_FLYWHEEL_NAMES[0]).toBe("计划飞轮");
  });

  it("六飞轮第6=考试飞轮", () => {
    expect(SIX_FLYWHEEL_NAMES[5]).toBe("考试飞轮");
  });

  it("六飞轮无错题/笔记/阅读/实践", () => {
    const forbidden = ["错题", "笔记", "阅读", "实践"];
    for (const name of SIX_FLYWHEEL_NAMES) {
      for (const word of forbidden) {
        expect(name).not.toContain(word);
      }
    }
  });

  it("七阶共 7 个", () => {
    expect(MASTERY_STAGE_NAMES).toHaveLength(7);
  });

  it("七阶首=不会, 末=创新", () => {
    expect(MASTERY_STAGE_NAMES[0]).toBe("不会");
    expect(MASTERY_STAGE_NAMES[6]).toBe("创新");
  });

  it("MECE 4维标签 = 动机/执行/能力/环境", () => {
    expect(MECE_LABELS.M).toBe("动机");
    expect(MECE_LABELS.E).toBe("执行");
    expect(MECE_LABELS.C).toBe("能力");
    expect(MECE_LABELS.E2).toBe("环境");
  });
});
