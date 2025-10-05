"""
Django settings for schul_lizenzen project.
"""

from pathlib import Path

# Basisverzeichnis des Projekts
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-ersetze-diesen-string-durch-einen-geheimen"
DEBUG = True   # Lokale Entwicklung
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

# Für Dev sicherstellen, dass Cookies auch über HTTP gesetzt werden:
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Installierte Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "lizenzen",  # deine App
    "widget_tweaks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "schul_lizenzen.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # globaler Template-Ordner
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "schul_lizenzen.wsgi.application"

# Datenbank – aktuell MySQL (wie wir konfiguriert haben)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "schul_lizenzen",
        "USER": "django_user",
        "PASSWORD": "roller123",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}

# Passwortvalidierung
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Sprache und Zeitzone
LANGUAGE_CODE = "de-ch"
TIME_ZONE = "Europe/Zurich"
USE_I18N = True
USE_TZ = True

# Statische Dateien (CSS, JS, Bilder)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Standard Primärschlüsseltyp
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
