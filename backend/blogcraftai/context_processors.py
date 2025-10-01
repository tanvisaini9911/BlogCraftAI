from __future__ import annotations

import json
from urllib.parse import urljoin

from django.conf import settings
from django.templatetags.static import static


def _absolute_static(request, path: str) -> str:
    relative = static(path)
    if request is None:
        return urljoin(settings.SITE_URL + "/", relative.lstrip("/"))
    return request.build_absolute_uri(relative)


def seo_defaults(request):
    """Provide base metadata to templates for SEO/GEO defaults."""

    site_url = settings.SITE_URL.rstrip("/") or "http://127.0.0.1:8000"
    canonical = request.build_absolute_uri() if request is not None else site_url
    canonical = canonical.split("#", 1)[0]

    default_image = settings.SEO_DEFAULT_IMAGE.strip() or _absolute_static(request, "img/og-default.svg")

    website_schema = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": settings.SITE_NAME,
            "url": site_url,
            "description": settings.SITE_DESCRIPTION,
            "potentialAction": {
                "@type": "SearchAction",
                "target": f"{site_url}/?q={{search_term_string}}",
                "query-input": "required name=search_term_string",
            },
        }
    )

    return {
        "site_meta": {
            "site_name": settings.SITE_NAME,
            "site_description": settings.SITE_DESCRIPTION,
            "site_url": site_url,
            "default_image": default_image,
            "website_schema": website_schema,
        },
        "canonical_url": canonical,
        "default_meta_robots": "index,follow",
    }

