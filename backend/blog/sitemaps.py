from __future__ import annotations

from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status=Post.PUBLISHED)

    def lastmod(self, obj: Post):
        return obj.updated_at or obj.published_at

    def location(self, obj: Post) -> str:
        return obj.get_absolute_url()
