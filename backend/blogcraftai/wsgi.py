"""WSGI config for BlogCraftAI."""
from __future__ import annotations

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogcraftai.settings")

application = get_wsgi_application()
