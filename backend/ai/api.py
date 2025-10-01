"""API endpoints for AI powered features."""
from __future__ import annotations

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import AiSuggestionClientError, AiSuggestionError, AiSuggestionService


class SeoSuggestionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        payload = request.data
        service = AiSuggestionService()
        try:
            suggestions = service.generate_seo_suggestions(
                title=payload.get("title", ""),
                summary=payload.get("summary", ""),
                content=payload.get("content", ""),
            )
        except AiSuggestionClientError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except AiSuggestionError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(
            {
                "suggestions": [
                    {
                        "heading": suggestion.heading,
                        "description": suggestion.description,
                        "keywords": suggestion.keywords,
                        "risks": suggestion.risks,
                    }
                    for suggestion in suggestions
                ]
            }
        )
