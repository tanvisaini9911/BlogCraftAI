"""Django settings for the BlogCraftAI project."""
from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SITE_NAME = os.getenv("SITE_NAME", "BlogCraftAI")
SITE_DOMAIN = os.getenv("SITE_DOMAIN", "https://blogcraftai.onrender.com")
SITE_URL = os.getenv("SITE_URL", f"http://{SITE_DOMAIN}").rstrip('/')
SITE_DESCRIPTION = os.getenv("SITE_DESCRIPTION", "AI-assisted blogging platform")
SEO_DEFAULT_IMAGE = os.getenv("SEO_DEFAULT_IMAGE", "")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "insecure-development-key")
DJANGO_ENV = os.getenv("DJANGO_ENV", "development").lower()
debug_flag = os.getenv("DJANGO_DEBUG")
if debug_flag is not None:
    DEBUG = debug_flag.lower() in {"1", "true", "yes"}
else:
    DEBUG = DJANGO_ENV not in {"production", "prod"}

ALLOWED_HOSTS_ENV = os.getenv("DJANGO_ALLOWED_HOSTS")
if ALLOWED_HOSTS_ENV:
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_ENV.split(",") if host.strip()]
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]
    render_external_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    if render_external_hostname:
        ALLOWED_HOSTS.append(render_external_hostname)
    site_domain_host = SITE_DOMAIN.replace("https://", "").replace("http://", "").split("/")[0]
    if site_domain_host:
        ALLOWED_HOSTS.append(site_domain_host)

render_external_url = os.getenv("RENDER_EXTERNAL_URL")
if SITE_URL.startswith(("http://", "https://")):
    site_origin = SITE_URL
else:
    site_origin = f"https://{SITE_URL}"
csrf_env = [
    origin.strip()
    for origin in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
csrf_origins = [render_external_url, site_origin, *csrf_env]
CSRF_TRUSTED_ORIGINS = []
for origin in csrf_origins:
    if not origin:
        continue
    normalized = origin.rstrip("/")
    if not normalized.startswith(("http://", "https://")):
        normalized = f"https://{normalized.lstrip('/')}"
    if normalized not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(normalized)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "accounts",
    "blog",
    "ai",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "blogcraftai.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "blogcraftai.context_processors.seo_defaults",
            ],
        },
    }
]

WSGI_APPLICATION = "blogcraftai.wsgi.application"
ASGI_APPLICATION = "blogcraftai.asgi.application"

database_url = os.getenv("DATABASE_URL")
conn_max_age = int(os.getenv("POSTGRES_CONN_MAX_AGE", "60"))
if database_url:
    ssl_require = os.getenv("DATABASE_SSL_REQUIRE", "true").lower() in {"1", "true", "yes"}
    DATABASES = {
        "default": dj_database_url.config(
            default=database_url,
            conn_max_age=conn_max_age,
            ssl_require=ssl_require,
        )
    }
elif os.getenv("POSTGRES_DB"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
            "CONN_MAX_AGE": conn_max_age,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("JWT_ACCESS_MINUTES", "30"))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("JWT_REFRESH_DAYS", "7"))),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

LOGIN_REDIRECT_URL = "blog:post-list"
LOGOUT_REDIRECT_URL = "blog:post-list"
LOGIN_URL = "accounts:login"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = os.getenv("DJANGO_SECURE_SSL_REDIRECT", "true" if not DEBUG else "false").lower() in {"1", "true", "yes"}
SESSION_COOKIE_SECURE = os.getenv("DJANGO_SESSION_COOKIE_SECURE", "true" if not DEBUG else "false").lower() in {"1", "true", "yes"}
CSRF_COOKIE_SECURE = os.getenv("DJANGO_CSRF_COOKIE_SECURE", "true" if not DEBUG else "false").lower() in {"1", "true", "yes"}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(name)s %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
        "ai": {
            "handlers": ["console"],
            "level": os.getenv("AI_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}

AI_PROVIDER_URL = os.getenv("AI_PROVIDER_URL", "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyAtorpX3hHNDGEnKZqGa2eGiefEKl0kNSA")
AI_PROVIDER_TIMEOUT = float(os.getenv("AI_PROVIDER_TIMEOUT", "10"))

