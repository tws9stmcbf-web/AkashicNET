"""Source-status matching only; never infer scientific support or review state.

Vocabulary: validate_public_safe_endpoint_registry_v014.py::validate.
`evidence` is the continuity fixture alias for the registry's `evidence_status`.
"""
from __future__ import annotations

EVIDENCE_STATUSES = frozenset({"NOT_APPLICABLE", "UNASSESSED", "SOURCE_CLASSIFICATION_ONLY"})
EVIDENCE_FIELDS = ("evidence_status", "evidence")


def classification(row):
    if not isinstance(row, dict):
        return None
    values = [row[key] for key in EVIDENCE_FIELDS if key in row]
    if not values or any(not isinstance(value, str) or value not in EVIDENCE_STATUSES
                         for value in values):
        return None
    return values[0] if all(value == values[0] for value in values) else None


def edge_classification(row):
    """An explicit edge status may not override conflicting representations.

    Without an edge status, every representation must have the same known
    status. Missing data is never silently labelled UNASSESSED.
    """
    explicit = any(key in row for key in EVIDENCE_FIELDS)
    status = classification(row)
    reps = row.get("representation_sources", [])
    if not isinstance(reps, list) or any(not isinstance(rep, dict) for rep in reps):
        return None
    supplied = [rep for rep in reps if any(key in rep for key in EVIDENCE_FIELDS)]
    if explicit:
        return status if status is not None and all(classification(rep) == status
                                                   for rep in supplied) else None
    statuses = [classification(rep) for rep in reps]
    if not statuses or statuses[0] is None:
        return None
    return statuses[0] if all(value == statuses[0] for value in statuses) else None
