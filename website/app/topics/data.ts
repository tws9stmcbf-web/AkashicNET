import seed from "../../../data/global_metadata_discovery_v01.seed.json";

export type TopicRecord = {
  id: string;
  slug: string;
  label: string;
  aliases: string[];
  domain: string;
  summary: string;
  status: "stub" | "discovery" | "reviewed" | "public";
  origin: {
    documentary_trace: string | null;
    ultimate_status: "known" | "partly-known" | "plural" | "contested" | "unresolved" | "unknown";
    claimed_origins: string[];
    evidence_note: string;
  };
  entities: Array<{
    id?: string;
    label: string;
    entity_status: string;
    ontological_status: string;
  }>;
  connections: Array<{
    target: string;
    relation: string;
    edge_status: string;
    source_ids: string[];
  }>;
  sources: Array<{
    id: string;
    url: string;
    source_type: string;
    evidence_role: string;
    retrieved_on?: string;
  }>;
  rights: {
    mode: string;
    license: string | null;
    note: string;
  };
  open_questions: string[];
  solution_space?: {
    status: "not-assessed" | "discovery" | "reviewed";
    quality_dimensions: string[];
    candidates: Array<{
      label: string;
      level: "individual" | "community" | "institutional" | "policy" | "ecological" | "multi-level";
      evidence_status: "established" | "supported" | "mixed" | "hypothesised" | "traditional-practice" | "unassessed";
      potential_benefits: string[];
      tradeoffs: string[];
      source_ids: string[];
    }>;
  };
  review: {
    human_reviewed: boolean;
    last_reviewed: string | null;
    notes: string;
  };
};

export const topicSeed = seed as unknown as {
  schema_version: string;
  registries: Array<{ id: string; name: string; url: string }>;
  topics: TopicRecord[];
};

export const topics = [...topicSeed.topics].sort((a, b) =>
  a.label.localeCompare(b.label),
);

export function findTopic(slug: string) {
  return topics.find((topic) => topic.slug === slug);
}

export function labelForSlug(slug: string) {
  return findTopic(slug)?.label ?? slug.replaceAll("-", " ");
}
