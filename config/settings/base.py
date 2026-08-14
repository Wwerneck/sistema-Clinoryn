import os
from pathlib import Path
from urllib.parse import unquote, urlparse

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-development-key")
DEBUG = False
ALLOWED_HOSTS = [item.strip() for item in os.getenv("ALLOWED_HOSTS", "").split(",") if item.strip()]
CSRF_TRUSTED_ORIGINS = [item.strip() for item in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if item.strip()]
DEMO_MODE = os.getenv("DEMO_MODE", "False").lower() == "true"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "accounts",
    "api",
    "dashboards",
    "especialidades",
    "pacientes",
    "medicos",
    "recepcao",
    "agenda",
    "consultas",
    "prontuarios",
    "prescricoes",
    "exames",
    "financeiro",
    "auditoria",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "auditoria.middleware.AuditContextMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "config.middleware.DemoReadOnlyMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "config.context_processors.demo_mode",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"

DATABASE_CONN_MAX_AGE = int(os.getenv("DATABASE_CONN_MAX_AGE", "60"))
DATABASE_URL = os.getenv("DATABASE_URL", "")


def _database_from_url(database_url):
    parsed = urlparse(database_url)
    if parsed.scheme not in {"postgres", "postgresql"}:
        raise ValueError("DATABASE_URL deve usar o esquema postgres ou postgresql.")

    database_name = unquote(parsed.path.lstrip("/"))
    if not database_name:
        raise ValueError("DATABASE_URL precisa informar o nome do banco de dados.")

    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": database_name,
        "USER": unquote(parsed.username or ""),
        "PASSWORD": unquote(parsed.password or ""),
        "HOST": parsed.hostname or "",
        "PORT": str(parsed.port or 5432),
        "CONN_MAX_AGE": DATABASE_CONN_MAX_AGE,
    }


if DATABASE_URL:
    DATABASES = {"default": _database_from_url(DATABASE_URL)}
elif os.getenv("DATABASE_ENGINE", "postgresql") == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {"default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME", "medagenda"),
        "USER": os.getenv("DATABASE_USER", "medagenda"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", "medagenda"),
        "HOST": os.getenv("DATABASE_HOST", "localhost"),
        "PORT": os.getenv("DATABASE_PORT", "5432"),
        "CONN_MAX_AGE": DATABASE_CONN_MAX_AGE,
    }}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "dashboards:home"
LOGOUT_REDIRECT_URL = "accounts:login"
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
REFERRER_POLICY = "same-origin"
CORS_ALLOWED_ORIGINS = [
    item.strip()
    for item in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if item.strip()
]
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "False").lower() == "true"
API_DOCS_REQUIRE_AUTH = os.getenv("API_DOCS_REQUIRE_AUTH", "False").lower() == "true"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "api.pagination.DefaultPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "user": os.getenv("DRF_USER_THROTTLE_RATE", "1000/day"),
        "anon": os.getenv("DRF_ANON_THROTTLE_RATE", "100/day"),
    },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Clinoryn API",
    "DESCRIPTION": "API REST versionada para a plataforma Clinoryn.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
    "ENUM_NAME_OVERRIDES": {
        "ConsultaStatusEnum": [
            ("AGENDADA", "Agendada"),
            ("CONFIRMADA", "Confirmada"),
            ("PACIENTE_CHEGOU", "Paciente chegou"),
            ("AGUARDANDO", "Aguardando"),
            ("EM_ATENDIMENTO", "Em atendimento"),
            ("CONCLUIDA", "Concluída"),
            ("CANCELADA", "Cancelada"),
            ("NAO_COMPARECEU", "Não compareceu"),
        ],
        "PagamentoStatusEnum": [
            ("PENDENTE", "Pendente"),
            ("PAGO", "Pago"),
            ("CANCELADO", "Cancelado"),
            ("ESTORNADO", "Estornado"),
        ],
        "PagamentoFormaEnum": [
            ("PIX", "Pix"),
            ("DINHEIRO", "Dinheiro"),
            ("CARTAO_CREDITO", "Cartão de crédito"),
            ("CARTAO_DEBITO", "Cartão de débito"),
            ("CONVENIO", "Convênio"),
            ("OUTRO", "Outro"),
        ],
    },
}
