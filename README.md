# OCEANZ STEM HUB

Website and learning platform for OCEANZ STEM HUB: Mathematics, Science and Coding/Digital
Technologies (M.S.C) for Primary, Secondary and Tertiary learners, following the Nigerian
school curriculum.

- Requirements: SRS v3.1, with the agreed changes in [docs/decisions.md](docs/decisions.md).
- Stack: Python 3.13, Django 5.2 LTS, PostgreSQL 17, Redis, Docker.

## Project layout

```
config/            settings (base, development, production), urls, wsgi
apps/core/         public site, CMS, health check
apps/accounts/     custom user model (public UUID, optional unique email, Argon2id)
requirements/      *.in (what we depend on), *.txt (exact versions, generated)
docs/              decisions and technical documentation
```

Further apps (academics, enrolment, payments, classroom, assessments and so on) are added in
the release that needs them, following the SRS roadmap R1 to R6.

## Run locally with Docker

```bash
cp .env.example .env
```

Edit `.env` and replace every `change-me` value. If port 5432 is already used on your
machine, set `POSTGRES_PORT` (and the port in `DATABASE_URL`) to a free port such as 5433.

```bash
docker compose up --build
```

The `migrate` service applies migrations, then `web` starts on http://127.0.0.1:8000.
Health check: http://127.0.0.1:8000/health/

Create a Super Admin account:

```bash
docker compose run --rm web python manage.py createsuperuser
```

The Django admin is at `/<DJANGO_ADMIN_URL>/`.

## Develop and test on the host

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements/dev.txt
docker compose up -d db redis
.venv/Scripts/python -m pytest
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m ruff format --check .
.venv/Scripts/pre-commit install
```

## Dependencies

`requirements/base.in` and `requirements/dev.in` list the packages we use, without versions
(Django is kept on the LTS line). `requirements/base.txt` and `requirements/dev.txt` are
generated from them with exact versions; Docker, CI and the local venv install from the
`.txt` files, so every environment runs the same versions. Never edit the `.txt` files by hand.

Add a package: add it to the right `.in` file, then compile. Upgrade everything to the latest
versions:

```bash
.venv/Scripts/python -m piptools compile --strip-extras --upgrade -o requirements/base.txt requirements/base.in
```
```bash
.venv/Scripts/python -m piptools compile --strip-extras --upgrade -o requirements/dev.txt requirements/dev.in
```
```bash
.venv/Scripts/python -m pip install -r requirements/dev.txt
```

Then run the tests and rebuild the Docker image before committing both `.in` and `.txt` files.

## Build and push the Docker image

```bash
docker build -t <dockerhub-user>/oceanz-stem-hub:<version> .
docker push <dockerhub-user>/oceanz-stem-hub:<version>
```

## Production (Render)

- Image: the Docker Hub image above, `DJANGO_SETTINGS_MODULE=config.settings.production`.
- Pre-deploy command: `python manage.py migrate --noinput`
- Health check path: `/health/`
- Required environment: `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`,
  `DJANGO_CSRF_TRUSTED_ORIGINS`, `DJANGO_ADMIN_URL`, `DATABASE_URL`, `REDIS_URL`,
  `TURNSTILE_SITE_KEY`, `TURNSTILE_SECRET_KEY` (Cloudflare Turnstile),
  `EMAIL_URL` (e.g. `smtp+tls://user:password@smtp-relay.brevo.com:587`), `DEFAULT_FROM_EMAIL`,
  and `RATELIMIT_IP_META_KEY` (e.g. `HTTP_CF_CONNECTING_IP` behind Cloudflare).
- `python manage.py check --deploy` fails while Turnstile uses test keys or email is not
  configured, so a misconfigured release is caught before it goes live.

## Local email and Turnstile

Locally, emails are printed in the web container log (`docker compose logs web`) and the forms
use Cloudflare's published Turnstile test keys, which always pass.
