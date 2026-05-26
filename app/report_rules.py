"""Shared report word-limit rules (used by validation and OOP validators)."""


def word_count(text: str) -> int:
    return len(text.split())


def validate_report(text: str) -> str | None:
    if not text or not text.strip():
        return "Report is required."
    if word_count(text) > 100:
        return f"Report must be at most 100 words (you entered {word_count(text)})."
    return None
