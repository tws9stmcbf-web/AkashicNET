function isDate(value) {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const date = new Date(value);
  return Number.isFinite(date.getTime()) && date.toISOString().slice(0, 10) === value;
}

// Display clearance is separate from evidence review and never inferred from status.
export function isPublicTopic(topic) {
  const clearance = topic.public_clearance;
  if (!clearance || clearance.decision !== "CLEARED" ||
      !isDate(clearance.reviewed_on) ||
      typeof clearance.decision_ref !== "string" || !clearance.decision_ref.trim() ||
      clearance.privacy_checked !== true || clearance.rights_checked !== true ||
      clearance.cultural_sovereignty_checked !== true) return false;
  if (!["stub", "discovery", "reviewed", "public"].includes(topic.status) ||
      !["metadata-only", "link-only", "licensed-reuse", "public-domain"].includes(topic.rights?.mode)) return false;
  if (["reviewed", "public"].includes(topic.status) &&
      (topic.review?.human_reviewed !== true || !isDate(topic.review.last_reviewed) || !topic.sources?.length)) return false;
  return topic.status !== "public" || topic.rights.mode !== "metadata-only";
}
