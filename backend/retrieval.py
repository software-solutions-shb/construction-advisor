"""Simple retrieval logic for Phase 1 (no embeddings).

We use basic keyword overlap + tag matches to rank entries.
Later this module can be replaced by a vector search approach.
"""

from __future__ import annotations

import re
from collections import Counter

from models import KnowledgeEntry

WORD_PATTERN = re.compile(r"[a-zA-Z0-9']+")


def _tokenize(text: str) -> list[str]:
    return WORD_PATTERN.findall(text.lower())


def _score_entry(question: str, entry: KnowledgeEntry) -> float:
    """Score relevance based on tag match and token overlap."""

    q_tokens = set(_tokenize(question))

    tag_bonus = 0
    for tag in entry.tags:
        if tag.lower() in q_tokens:
            tag_bonus += 3

    # Compare against entry question and section content
    entry_text = " ".join([
        entry.question,
        " ".join(entry.sections.values()),
        entry.extra_context or "",
    ])

    entry_tokens = set(_tokenize(entry_text))
    overlap = q_tokens.intersection(entry_tokens)

    return tag_bonus + len(overlap)


def retrieve_relevant_entries(
    question: str,
    entries: list[KnowledgeEntry],
    limit: int = 3,
) -> list[KnowledgeEntry]:
    """Return top entries by simple heuristic relevance score."""

    scored = [(entry, _score_entry(question, entry)) for entry in entries]
    scored.sort(key=lambda pair: pair[1], reverse=True)

    # If everything scores 0, still return the first few entries for context.
    top = [entry for entry, _ in scored[:limit]]
    return top
