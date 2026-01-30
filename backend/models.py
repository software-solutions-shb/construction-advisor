"""Shared data models for knowledge base entries."""

from dataclasses import dataclass, field


@dataclass
class KnowledgeEntry:
    """Represents one approved advisory entry parsed from Markdown."""

    file_path: str
    id: str
    question: str
    tags: list[str]
    risk_level: str
    reviewer: str
    source: str
    images: list[str]
    sections: dict[str, str] = field(default_factory=dict)
    extra_context: str = ""
    raw_text: str = ""
