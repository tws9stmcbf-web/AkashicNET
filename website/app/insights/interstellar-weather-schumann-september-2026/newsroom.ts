export const NEWSROOM_SNAPSHOT_TIMESTAMP = "2026-09-14T13:18:18.794Z";
export const NEWSROOM_WINDOW_HOURS = 24;

export const NEWSROOM_CATEGORIES = [
  "Global Challenges",
  "AI & Technology",
  "Earth-Space Weather",
  "Evidence Desk",
  "Kindness Across Species",
] as const;

export const NEWSROOM_EVIDENCE_LABELS = [
  "Established Evidence",
  "Observation",
  "Interpretation",
  "Lived Experience/Testimony",
  "Hypothesis",
  "Speculation",
] as const;

export const NEWSROOM_STATUSES = ["PUBLIC", "REVIEW", "WITHHELD", "ARCHIVE"] as const;
export const KINDNESS_HEADINGS = ["Habitat Restored", "Wildlife Rescued", "Communities Cooperating"] as const;

export type NewsroomCategory = (typeof NEWSROOM_CATEGORIES)[number];
export type NewsroomEvidenceLabel = (typeof NEWSROOM_EVIDENCE_LABELS)[number];
export type NewsroomStatus = (typeof NEWSROOM_STATUSES)[number];
export type KindnessHeading = (typeof KINDNESS_HEADINGS)[number];

export type NewsroomItem = {
  readonly id: string;
  readonly headline: string;
  readonly shortSummary: string;
  readonly category: NewsroomCategory;
  readonly sourceUrl: string;
  readonly sourceTimestamp: string;
  readonly publishedAt: string;
  readonly updatedAt: string;
  readonly evidenceLabel: NewsroomEvidenceLabel;
  readonly status: NewsroomStatus;
  readonly kindnessHeading?: KindnessHeading;
};

export const CANONICAL_13D_SEQUENCE = [
  "AWAKEN",
  "HIERATIC",
  "HOMESENSE",
  "ADAPT",
  "REGENERATE",
  "TRANSCEND",
  "#METAD v2.1",
  "ACTC",
  "MultidimensionalCUT · PAST",
  "MultidimensionalCUT · PRESENT",
  "MultidimensionalCUT · FUTURE",
  "UMASC",
  "AKASHICNET",
] as const;

export const INSIGHTS_DIMENSIONS: ReadonlyArray<readonly [string, (typeof CANONICAL_13D_SEQUENCE)[number], string]> = [
  ["01", "AWAKEN", "Notice the disturbance without deciding what it means."],
  ["02", "HIERATIC", "Explore Earth as a living resonant symbol and preserve spiritual meaning as interpretation."],
  ["03", "HOMESENSE", "Listen to sleep, mood, dream and somatic testimony as lived experience."],
  ["04", "ADAPT", "Separate source signal, explanatory story and plausible confounders."],
  ["05", "REGENERATE", "Respond with rest, grounding, reflection and compassionate care."],
  ["06", "TRANSCEND", "Place Sun, Pachamama, biosphere and consciousness within a wider system."],
  ["07", "#METAD v2.1", "Compare competing explanations and search for contradictions."],
  ["08", "ACTC", "Map agency, context, temporal order and candidate causal pathways."],
  ["09", "MultidimensionalCUT · PAST", "Compare prior solar, geomagnetic, lunar and resonance patterns."],
  ["10", "MultidimensionalCUT · PRESENT", "Describe the dated 11–12 September activity window precisely."],
  ["11", "MultidimensionalCUT · FUTURE", "Pre-register what to measure during the next comparable event."],
  ["12", "UMASC", "Relate matter, awareness, systems and culture without collapsing their differences."],
  ["13", "AKASHICNET", "Synthesize the whole field while leaving unresolved questions open."],
];

export const INSIGHTS_NEWSROOM_ITEMS: readonly NewsroomItem[] = [
  {
    id: "ai-technology-human-governance-boundary",
    headline: "Human-governed AI remains the public rule, not autonomy theatre.",
    shortSummary:
      "The public About and homepage language still places compassion, privacy and human accountability above scale or automation; this is a boundary statement, not evidence of safe autonomy.",
    category: "AI & Technology",
    sourceUrl: "https://akashicnet.org/about",
    sourceTimestamp: "2026-08-30T00:00:00Z",
    publishedAt: "2026-09-14T08:45:00Z",
    updatedAt: "2026-09-14T08:45:00Z",
    evidenceLabel: "Interpretation",
    status: "PUBLIC",
  },
  {
    id: "earth-space-weather-static-window-boundary",
    headline: "The Schumann page remains a dated activity-window report, not live telemetry.",
    shortSummary:
      "The current Insights source is a static 11–12 September analysis reviewed after conditions returned quiet; Schumann resonance, Kp context, solar conditions and symbolic OM imagery stay separate analytical layers.",
    category: "Earth-Space Weather",
    sourceUrl: "https://akashicnet.org/insights/interstellar-weather-schumann-september-2026",
    sourceTimestamp: "2026-09-14T00:00:00Z",
    publishedAt: "2026-09-14T09:10:00Z",
    updatedAt: "2026-09-14T09:10:00Z",
    evidenceLabel: "Observation",
    status: "PUBLIC",
  },
  {
    id: "evidence-desk-akashicomni-governance-release",
    headline: "AkashicOMNI v0.3.0 keeps framework updates explicit and non-retroactive.",
    shortSummary:
      "The current public release note says version changes follow method changes and preserve earlier assessments rather than silently promoting truth, evidence or framework status.",
    category: "Evidence Desk",
    sourceUrl: "https://akashicnet.org/akashicomni#v0-3-0",
    sourceTimestamp: "2026-09-14T00:00:00Z",
    publishedAt: "2026-09-14T10:20:00Z",
    updatedAt: "2026-09-14T10:20:00Z",
    evidenceLabel: "Observation",
    status: "PUBLIC",
  },
  {
    id: "kindness-across-species-placeholder",
    headline: "Hold hopeful habitat coverage until a verified public source lands in the repository.",
    shortSummary:
      "The public repository does not yet contain a current, publishable habitat-restoration or wildlife-rescue source record for this 24-hour window, so the kindness segment fails closed instead of improvising a feel-good claim.",
    category: "Kindness Across Species",
    sourceUrl: "https://akashicnet.org/community",
    sourceTimestamp: "2026-08-30T00:00:00Z",
    publishedAt: "2026-09-13T06:00:00Z",
    updatedAt: "2026-09-13T06:00:00Z",
    evidenceLabel: "Observation",
    status: "ARCHIVE",
    kindnessHeading: "Communities Cooperating",
  },
] as const;

const UTC_ISO_PATTERN = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/;

function parseUtcTimestamp(value: string): number | null {
  if (!UTC_ISO_PATTERN.test(value)) return null;
  const parsed = Date.parse(value);
  return Number.isNaN(parsed) ? null : parsed;
}

export function isPublicSourceUrl(value: string): boolean {
  try {
    const url = new URL(value);
    return url.protocol === "https:" && Boolean(url.hostname);
  } catch {
    return false;
  }
}

export function isPublishableNewsroomItem(item: NewsroomItem, nowTimestamp = NEWSROOM_SNAPSHOT_TIMESTAMP): boolean {
  if (item.status !== "PUBLIC") return false;
  if (!item.headline.trim() || !item.shortSummary.trim() || !item.evidenceLabel.trim()) return false;
  if (!isPublicSourceUrl(item.sourceUrl)) return false;

  const sourceMs = parseUtcTimestamp(item.sourceTimestamp);
  const publishedMs = parseUtcTimestamp(item.publishedAt);
  const updatedMs = parseUtcTimestamp(item.updatedAt);
  const nowMs = parseUtcTimestamp(nowTimestamp);
  if (sourceMs === null || publishedMs === null || updatedMs === null || nowMs === null) return false;
  if (sourceMs > publishedMs || publishedMs > updatedMs || updatedMs > nowMs) return false;

  const windowStart = nowMs - NEWSROOM_WINDOW_HOURS * 60 * 60 * 1000;
  if (publishedMs < windowStart || updatedMs < windowStart) return false;

  return true;
}

export function getPublishableNewsroomItems(nowTimestamp = NEWSROOM_SNAPSHOT_TIMESTAMP): NewsroomItem[] {
  return [...INSIGHTS_NEWSROOM_ITEMS]
    .filter((item) => isPublishableNewsroomItem(item, nowTimestamp))
    .sort((left, right) => Date.parse(right.updatedAt) - Date.parse(left.updatedAt));
}

export function getKindnessAcrossSpeciesItems(nowTimestamp = NEWSROOM_SNAPSHOT_TIMESTAMP): NewsroomItem[] {
  return getPublishableNewsroomItems(nowTimestamp).filter((item) => item.category === "Kindness Across Species");
}
