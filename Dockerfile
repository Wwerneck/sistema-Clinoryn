FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN addgroup --system medagenda && adduser --system --ingroup medagenda medagenda
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x /app/docker/entrypoint.sh && mkdir -p /app/staticfiles /app/media/private && chown -R medagenda:medagenda /app

USER medagenda
EXPOSE 8000
ENTRYPOINT ["/app/docker/entrypoint.sh"]
