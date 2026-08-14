from .base import *  # noqa: F403

if len(SECRET_KEY) < 32 or SECRET_KEY.startswith(("unsafe", "troque")):  # noqa: F405
    raise RuntimeError("SECRET_KEY forte deve ser configurada em produção.")
if os.getenv("DATABASE_ENGINE", "postgresql") != "postgresql":  # noqa: F405
    raise RuntimeError("O ambiente de produção exige PostgreSQL.")

SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True").lower() == "true"  # noqa: F405
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
DEBUG = False
ALLOWED_HOSTS = [item.strip() for item in os.getenv("ALLOWED_HOSTS", "").split(",") if item.strip()]  # noqa: F405
SECURE_REDIRECT_EXEMPT = [r"^health/"]
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

render_external_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")  # noqa: F405
if render_external_hostname:
    if render_external_hostname not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(render_external_hostname)
    render_origin = f"https://{render_external_hostname}"
    if render_origin not in CSRF_TRUSTED_ORIGINS:  # noqa: F405
        CSRF_TRUSTED_ORIGINS.append(render_origin)  # noqa: F405

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"jsonlike": {"format": "{asctime} {levelname} {name} {message}", "style": "{"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "jsonlike"}},
    "root": {"handlers": ["console"], "level": os.getenv("LOG_LEVEL", "INFO")},  # noqa: F405
}
