from pathlib import Path
import os

import cloudinary
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name, default=""):
    raw_value = os.environ.get(name, default)
    return [item.strip() for item in raw_value.split(",") if item.strip()]


SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY deve ser configurada no arquivo .env ou no ambiente.")

DEBUG = env_bool("DEBUG", default=False)
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1,testserver")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")


INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "cloudinary_storage",
    "cloudinary",
    "django_ckeditor_5",

    "apps.ong",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "apps.ong.middleware.AdminGroupRequiredMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "capiclima.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.ong.context_processors.configuracao_site",
            ],
        },
    },
]

WSGI_APPLICATION = "capiclima.wsgi.application"


if os.environ.get("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            default=os.environ.get("DATABASE_URL"),
            conn_max_age=600,
            conn_health_checks=True,
        )
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


LANGUAGE_CODE = "pt-br"
TIME_ZONE = os.environ.get("TIME_ZONE", "America/Cuiaba")
USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET")
CLOUDINARY_CONFIGURED = all(
    [CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]
)

if CLOUDINARY_CONFIGURED:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
        secure=True,
    )

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,
    "API_KEY": CLOUDINARY_API_KEY,
    "API_SECRET": CLOUDINARY_API_SECRET,
}

DEFAULT_FILE_STORAGE_BACKEND = (
    "cloudinary_storage.storage.MediaCloudinaryStorage"
    if CLOUDINARY_CONFIGURED
    else "django.core.files.storage.FileSystemStorage"
)

STORAGES = {
    "default": {"BACKEND": DEFAULT_FILE_STORAGE_BACKEND},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "underline",
            "strikethrough",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "link",
            "blockQuote",
            "|",
            "undo",
            "redo",
        ],
        "language": "pt-br",
    },
}

CKEDITOR_5_FILE_STORAGE = DEFAULT_FILE_STORAGE_BACKEND
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
CKEDITOR_5_UPLOAD_FILE_TYPES = ["jpg", "jpeg", "png", "webp"]
CKEDITOR_5_MAX_FILE_SIZE = 5


JAZZMIN_SETTINGS = {
    "site_title": "CapiClima Admin",
    "site_header": "CapiClima",
    "site_brand": "CapiClima",
    "welcome_sign": "Painel de gerenciamento do CapiClima",
    "copyright": "CapiClima",

    "search_model": [
        "ong.Atividade",
        "ong.MembroEquipe",
        "ong.Opportunity",
    ],

    "topmenu_links": [
        {
            "name": "Ver site",
            "url": "/",
            "new_window": True,
        },
        {
            "name": "Admin",
            "url": "admin:index",
            "permissions": ["auth.view_user"],
        },
    ],

    "show_sidebar": True,
    "navigation_expanded": True,

    "hide_apps": [],
    "hide_models": [
        "auth.Group",
    ],

    "order_with_respect_to": [
        "ong.DestaqueInicio",
        "ong.Parceiro",
        "ong.Atividade",
        "ong.Opportunity",
        "ong.MembroEquipe",
        "ong.SecaoApoie",
        "ong.SiteConfig",
        "auth.User",
    ],

    "icons": {
        "auth.User": "fas fa-user",
        "ong.DestaqueInicio": "fas fa-images",
        "ong.Parceiro": "fas fa-handshake",
        "ong.Atividade": "fas fa-leaf",
        "ong.Opportunity": "fas fa-table",
        "ong.MembroEquipe": "fas fa-users",
        "ong.SecaoApoie": "fas fa-heart",
        "ong.SiteConfig": "fas fa-cog",
    },
}


JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": None,
    "navbar": "navbar-white navbar-light",
    "sidebar": "sidebar-dark-success",
    "brand_colour": "navbar-success",
    "accent": "accent-success",
    "button_classes": {
        "primary": "btn-success",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}


# Security settings for production
if not DEBUG:
    # HTTPS and security headers
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_SECURITY_POLICY = {
        "default-src": ("'self'",),
        "script-src": ("'self'", "cdn.jsdelivr.net", "code.jquery.com"),
        "style-src": ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net"),
        "img-src": ("'self'", "data:", "https:", "res.cloudinary.com"),
        "font-src": ("'self'", "cdn.jsdelivr.net"),
        "connect-src": ("'self'", "res.cloudinary.com"),
    }
    
    # WhiteNoise cache configuration
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
