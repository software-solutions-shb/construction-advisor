"""Ollama LLaMA client and prompt builder.

This keeps LLM interaction isolated so we can replace it later.
"""

from __future__ import annotations

import os
import textwrap
import requests

from models import KnowledgeEntry


def _build_context_block(entry: KnowledgeEntry) -> str:
    """Format a knowledge entry into a block the LLM can read easily."""

    def section(title: str) -> str:
        content = entry.sections.get(title, "").strip()
        if not content:
            return ""
        return f"## {title}\n{content}\n"

    parts = [
        f"ID: {entry.id}",
        f"Question: {entry.question}",
        f"Tags: {', '.join(entry.tags)}",
        f"Risk: {entry.risk_level}",
        "",
        section("Summary of the situation"),
        section("Key considerations"),
        section("Options and trade-offs"),
        section("Suggested next steps"),
        section("Boundaries disclaimer"),
        section("Assumptions"),
        section("Escalation notes"),
    ]

    if entry.extra_context:
        parts.append("## Added context notes\n" + entry.extra_context.strip())

    return "\n".join([p for p in parts if p])


def _build_prompt(question: str, entries: list[KnowledgeEntry], image_refs: list[str]) -> str:
    """Build a full prompt for the LLM with all relevant context."""

    context_blocks = "\n\n".join(_build_context_block(entry) for entry in entries)

    image_note = ""
    if image_refs:
        image_note = "User provided image references: " + ", ".join(image_refs)

    system_style = textwrap.dedent(
        """
        You are Alex, an experienced construction and kitchen advisor with 30+ years of industry experience.
        You provide calm, practical, conservative guidance and a second opinion.
        You are NOT an inspector, engineer, permit authority, or legal advisor.
        Do not certify compliance, approve work, or guarantee outcomes.
        If the situation requires on-site inspection, licensed engineering, or legal advice, say so clearly.
        Use plain language and structure your response with headings and bullet points.
        """
    ).strip()

    return textwrap.dedent(
        f"""
        {system_style}

        {image_note}

        Relevant approved knowledge (use carefully and cite assumptions or limits):
        {context_blocks}

        User question:
        {question}

        Respond in this format:
        1) Summary of the situation
        2) Key considerations
        3) Options and trade-offs
        4) Suggested next steps
        5) Boundaries disclaimer
        6) Assumptions
        7) Escalation notes
        """
    ).strip()


def generate_answer(question: str, entries: list[KnowledgeEntry], image_refs: list[str]) -> str:
    """Call the local Ollama API to generate a response."""

    prompt = _build_prompt(question, entries, image_refs)

    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    model_name = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(ollama_url, json=payload, timeout=120)
    if response.status_code != 200:
        raise RuntimeError(f"Ollama error: {response.status_code} {response.text}")

    data = response.json()
    return data.get("response", "").strip()
