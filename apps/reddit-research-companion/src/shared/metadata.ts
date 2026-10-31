export type MetadataObservation = {
  post_id: string;
  observed_at: string;
  lookup_status: 'observed' | 'unavailable' | 'suppressed' | 'out_of_scope' | 'retry';
  metadata: null | {
    canonical_permalink: string; subreddit: string; title: string | null;
    flair: string | null; created_at: string | null; submitted_url: string | null;
    score_snapshot: number | null; comment_count_snapshot: number | null;
  };
};
export type MetadataBatch = {
  schema: 'akashicnet.devvit.metadata-batch.v1';
  mode: 'known-n2n' | 'this-post';
  target_subreddit: string;
  manifest_sha256: string;
  known_ids: number;
  from_cursor: number;
  next_cursor: number;
  pass_finished: boolean;
  retry_after_seconds: number;
  records: MetadataObservation[];
  public_merge_status: 'REVIEW_REQUIRED';
};
