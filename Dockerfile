FROM python:3.13-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

FROM base AS builder
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements/base.txt requirements/base.txt
RUN pip install -r requirements/base.txt

FROM base AS production
RUN groupadd --system app && useradd --system --gid app --no-create-home app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=config.settings.production \
    PORT=8000
COPY . .
# collectstatic needs settings to load; these values exist only for this build step.
RUN DJANGO_SECRET_KEY=collectstatic-only \
    DJANGO_ADMIN_URL=collectstatic-only \
    DATABASE_URL=postgres://build@localhost/build \
    REDIS_URL=redis://localhost:6379/0 \
    python manage.py collectstatic --noinput
USER app
EXPOSE 8000
CMD ["sh", "-c", "exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT} --workers ${WEB_CONCURRENCY:-3} --access-logfile -"]
