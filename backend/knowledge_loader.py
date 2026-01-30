"""Load and parse approved knowledge base Markdown files.

Assumes files are in knowledge/approved/ and contain YAML front matter
followed by sectioned content using Markdown headings.
"""

from __future__ import annotations

import os
import re
from typing import Iterable

import yaml

from models import KnowledgeEntry

# Known section headings used in the advisory template.
KNOWN_SECTIONS = [
    "Summary of the situation",
    "Key considerations",
    "Options and trade-offs",
    "Suggested next steps",
    "Boundaries disclaimer",
    "Assumptions",
    "Escalation notes",
]

SECTION_PATTERN = re.compile(r"^##\s+(.*)$", re.MULTILINE)


def _split_front_matter(text: str) -> tuple[dict, str]:
    """Split YAML front matter from the Markdown body.

    Returns (front_matter_dict, body_text).
    """

    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    front_matter_raw = parts[1]
    body = parts[2].lstrip()
    front_matter = yaml.safe_load(front_matter_raw) or {}
    return front_matter, body


def _parse_sections(body: str) -> tuple[dict[str, str], str]:
    """Parse known sections and capture any extra context at the bottom.

    The "extra_context" is any content after the last known section or any
    non-section text at the end. This is important and should be included
    in prompts later.
    """

    sections: dict[str, str] = {}

    # Find all section headings and their positions.
    matches = list(SECTION_PATTERN.finditer(body))
    if not matches:
        return sections, body.strip()

    for idx, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        if title in KNOWN_SECTIONS:
            sections[title] = content

    # Extra context = content after the last known section (if any).
    last_known_index = None
    for idx in reversed(range(len(matches))):
        if matches[idx].group(1).strip() in KNOWN_SECTIONS:
            last_known_index = idx
            break

    if last_known_index is None:
        extra_context = ""
    else:
        extra_context = body[matches[last_known_index].end():].strip()
        # Remove the content of the known section itself.
        known_title = matches[last_known_index].group(1).strip()
        if known_title in sections:
            extra_context = extra_context.replace(sections[known_title], "", 1).strip()

    return sections, extra_context


def _iter_markdown_files(folder_path: str) -> Iterable[str]:
    for root, _, files in os.walk(folder_path):
        for name in files:
            if name.lower().endswith(".md"):
                yield os.path.join(root, name)


def load_knowledge_base(base_path: str | None = None) -> list[KnowledgeEntry]:
    """Load all approved entries from knowledge/approved/.

    `base_path` can be overridden for testing. By default it uses the repo root.
    """

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    knowledge_root = base_path or os.path.join(repo_root, "knowledge", "approved")

    if not os.path.exists(knowledge_root):
        raise FileNotFoundError(
            "Knowledge base not found. Expected folder: knowledge/approved/"
        )

    entries: list[KnowledgeEntry] = []

    for file_path in _iter_markdown_files(knowledge_root):
        with open(file_path, "r", encoding="utf-8") as file:
            raw_text = file.read()

        front_matter, body = _split_front_matter(raw_text)
        sections, extra_context = _parse_sections(body)

        entry = KnowledgeEntry(
            file_path=file_path,
            id=str(front_matter.get("id", os.path.basename(file_path))),
            question=str(front_matter.get("question", "")),
            tags=list(front_matter.get("tags", [])),
            risk_level=str(front_matter.get("risk_level", "low")),
            reviewer=str(front_matter.get("reviewer", "")),
            source=str(front_matter.get("source", "")),
            images=list(front_matter.get("images", [])),
            sections=sections,
            extra_context=extra_context,
            raw_text=raw_text,
        )
        entries.append(entry)

    return entries
