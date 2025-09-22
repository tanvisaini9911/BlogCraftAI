"""Prompt-engineering aware integrations."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)


class AiSuggestionError(RuntimeError):
    """Raised when the AI suggestion provider returns an unexpected result."""


@dataclass(frozen=True)
class SeoSuggestion:
    heading: str
    description: str
    keywords: list[str]
    risks: list[str]

    @classmethod
    def from_payload(cls, payload: dict) -> "SeoSuggestion":
        if not isinstance(payload, dict):
            raise AiSuggestionError("Malformed suggestion payload.")
        try:
            heading = str(payload["heading"])
            description = str(payload["description"])
            keywords_raw = payload.get("keywords", [])
            if isinstance(keywords_raw, str):
                keywords = [kw.strip() for kw in keywords_raw.split(",") if kw.strip()]
            else:
                keywords = [str(kw) for kw in keywords_raw]
            risks_raw = payload.get("risks", [])
            if isinstance(risks_raw, str):
                risks = [risk.strip() for risk in risks_raw.split(",") if risk.strip()]
            else:
                risks = [str(risk) for risk in risks_raw]
        except KeyError as exc:
            raise AiSuggestionError(f"Missing expected field: {exc.args[0]}") from exc
        return cls(heading=heading, description=description, keywords=keywords, risks=risks)


class AiSuggestionService:
    """Service abstraction around the external AI suggestion provider."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        timeout: float | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url or settings.AI_PROVIDER_URL
        self.timeout = timeout or settings.AI_PROVIDER_TIMEOUT
        self._client = client or httpx.Client(timeout=self.timeout)

    def build_payload(self, *, title: str, summary: str, content: str) -> dict:
        if not title or not summary or not content:
            raise AiSuggestionError("Title, summary, and content are required for suggestions.")
        prompt = (
            "You are an SEO assistant. Provide actionable suggestions for blog optimisation "
            "including improved headings, meta descriptions, and keywords."
        )
        return {
            "prompt": prompt,
            "context": {
                "title": title,
                "summary": summary,
                "content": content,
            },
            "response_format": {
                "type": "object",
                "properties": {
                    "suggestions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "heading": {"type": "string"},
                                "description": {"type": "string"},
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "risks": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                        "required": ["heading", "description", "keywords"],
                    },
                }
            },
                "required": ["suggestions"],
            },
        }

    def generate_seo_suggestions(self, *, title: str, summary: str, content: str) -> list[SeoSuggestion]:
        payload = self.build_payload(title=title, summary=summary, content=content)
        try:
            response = self._client.post(self.base_url, json=payload, timeout=self.timeout)
            response.raise_for_status()
        except httpx.TimeoutException as exc:  # pragma: no cover - covered via tests raising error
            logger.error("AI provider timeout: %s", exc)
            raise AiSuggestionError("The AI provider timed out. Please try again.") from exc
        except httpx.HTTPStatusError as exc:
            logger.error("AI provider returned HTTP %s", exc.response.status_code)
            raise AiSuggestionError(
                f"AI provider error: HTTP {exc.response.status_code}"
            ) from exc
        except httpx.HTTPError as exc:
            logger.exception("Unexpected AI provider error")
            raise AiSuggestionError("Unable to contact the AI provider.") from exc

        try:
            payload = response.json()
        except json.JSONDecodeError as exc:
            logger.error("Invalid JSON from AI provider: %s", exc)
            raise AiSuggestionError("AI provider returned malformed data.") from exc

        suggestions_raw = payload.get("suggestions")
        if not isinstance(suggestions_raw, (list, tuple)):
            raise AiSuggestionError("AI provider did not return suggestions.")

        suggestions: list[SeoSuggestion] = []
        for item in suggestions_raw:
            suggestions.append(SeoSuggestion.from_payload(item))
        return suggestions

    def __del__(self):  # pragma: no cover - defensive cleanup
        try:
            self._client.close()
        except Exception:  # pragma: no cover
            logger.debug("Failed to close AI client", exc_info=True)
