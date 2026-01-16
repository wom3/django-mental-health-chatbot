# Copilot instructions (Django Mental Health Counseling Bot)

## Big picture

- This is a small Django app that serves a single-page chat UI and proxies user messages to the OpenAI API.
- Request flow: browser (AJAX POST) → `chatbot/views.py:chatbot_response` → OpenAI Chat Completions → JSON `{reply: ...}` → UI renders the reply.
- Templates live under `chatbot/templates/` and use Django template inheritance via `templates/base.html`.

## Key files

- Django settings/entrypoints: `chatbot_project/settings.py`, `chatbot_project/urls.py`, `manage.py`
- App routing + handler: `chatbot/urls.py`, `chatbot/views.py`
- Chat UI template: `chatbot/templates/chatbot/chat.html`
- Base template: `chatbot/templates/base.html`
- Dataset utilities (fine-tuning prep): `load_dataset.py`, `data/train.jsonl`, `data/validation.jsonl`, `solutions.ipynb`

## Local dev workflow

- Run the server (commonly used in this repo): `python3 manage.py runserver 0.0.0.0:8080`
- This repo uses a local virtualenv folder `.venv/` (already present). Prefer running commands in that environment.

## OpenAI integration conventions

- `chatbot/views.py` initializes the client with `OpenAI(api_key=os.getenv('OPENAI_API_KEY'))`.
- Credentials are expected in `.env` and loaded by `python-dotenv` in `chatbot_project/settings.py`.
  - Use env var name: `OPENAI_API_KEY`
  - Do not hardcode API keys in code/notebooks.
- The UI expects the view to return JSON with shape: `{ "reply": "..." }`.

## Template + frontend gotchas (important)

- Keep Django template tags on a single line (e.g., `{% block content %}`) — some HTML formatters can split `{% ... %}` across lines and break Django parsing.
- The chat UI uses jQuery AJAX; CSRF is passed by reading the hidden `csrfmiddlewaretoken` input inserted by `{% csrf_token %}`.

## Project-specific patterns

- The app currently does not define domain models (see `chatbot/models.py`). If you add models, also add `chatbot` to `INSTALLED_APPS` in `chatbot_project/settings.py` and create migrations.
- Template search paths include `BASE_DIR/chatbot/templates` (see `TEMPLATES[0]['DIRS']` in `chatbot_project/settings.py`).
