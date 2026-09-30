/** OMNI's documented role for ACTC; not a new definition of the underlying framework.
 * Source: website/app/akashicomni/page.tsx at af2e92c71d081f54c97e269bf683b0c45ac4c4c1.
 */
export const actcOmniDescription = "Agency, context, temporal order and candidate causes.";
export const expandPasses = [
  ["DISCERN", "Identify the question, sources, evidence type, assumptions, uncertainty and possible harm."],
  ["DEEPEN", "Revisit through contrasting lenses, seek disconfirming evidence, compare alternatives and clarify what changed."],
] as const;
export const synthesisOutput = "Report the synthesis, uncertainty, limits and next questions. The outcome may remain unresolved or warrant caution; a second pass does not guarantee stronger evidence.";
export const outcomeBoundary = "Outcome labels describe an interpretive assessment, not an evidence rating, confidence score or permission to promote a claim. Source-specific evidence status and uncertainty must be stated separately.";
