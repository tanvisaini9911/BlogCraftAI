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


class AiSuggestionClientError(AiSuggestionError):
    """Raised when the request payload is invalid for AI suggestions."""


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

    def _extract_candidate_text(self, payload: dict) -> str:
        candidates = payload.get("candidates")
        if not candidates:
            prompt_feedback = payload.get("promptFeedback") or {}
            block_reason = prompt_feedback.get("blockReason")
            if block_reason:
                raise AiSuggestionError(f"AI provider blocked the prompt: {block_reason}")
            raise AiSuggestionError("AI provider did not return any candidates.")
        for candidate in candidates:
            content = candidate.get("content") or {}
            parts = content.get("parts") or []
            texts = [part.get("text") for part in parts if isinstance(part, dict) and part.get("text")]
            combined = "".join(texts).strip()
            if combined:
                return combined
        raise AiSuggestionError("AI provider returned an empty response.")

    def _normalize_model_output(self, text: str) -> str:
        stripped = text.strip()
        if stripped.startswith("```") and stripped.endswith("```"):
            inner = stripped[3:-3].strip()
            if inner.lower().startswith("json"):
                inner = inner[4:].lstrip()
            stripped = inner
        stripped = stripped.strip()
        if stripped.startswith("{") and stripped.endswith("}"):
            return stripped
        first = stripped.find("{")
        last = stripped.rfind("}")
        if first != -1 and last != -1 and first < last:
            return stripped[first:last + 1].strip()
        return stripped

    def build_payload(self, *, title: str, summary: str, content: str) -> dict:
        title_value = str(title or "").strip()
        summary_value = str(summary or "").strip()
        content_value = str(content or "").strip()
        if not title_value or not summary_value or not content_value:
            raise AiSuggestionClientError("Title, summary, and content are required for suggestions.")

        prompt = (
            "You are an SEO assistant. Provide actionable suggestions for blog optimisation "
            "including improved headings, meta descriptions, and keywords. Return strictly valid JSON "
            "matching the schema: {\"suggestions\": [{\"heading\": string, \"description\": string, \"keywords\": [string], \"risks\": [string]}]} without extra commentary."
        )
        context_blob = json.dumps(
            {
                "title": title_value,
                "summary": summary_value,
                "content": content_value,
            },
            ensure_ascii=False,
        )
        message = f"{prompt}\nInput: {context_blob}"

        return {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": message}
                    ],
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
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
            data = response.json()
        except json.JSONDecodeError as exc:
            logger.error("Invalid JSON from AI provider: %s", exc)
            raise AiSuggestionError("AI provider returned malformed data.") from exc

        candidate_text = self._extract_candidate_text(data)
        normalized_text = self._normalize_model_output(candidate_text)
        try:
            payload = json.loads(normalized_text)
        except json.JSONDecodeError as exc:
            logger.error("Non-JSON AI provider payload: %s", normalized_text)
            raise AiSuggestionError("AI provider returned non-JSON suggestions.") from exc

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


