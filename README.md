# Django Mental Health Counseling Bot

A small Django app that serves a single-page chat UI and proxies user messages to the OpenAI API. It also includes scripts/notebooks for preparing a mental-health counseling dataset and (optionally) fine-tuning a chat model.

## Salient features

- Single-page chat UI with AJAX posting and live transcript updates
- Simple Django proxy endpoint returning a consistent JSON shape: `{ "reply": "..." }`
- Dataset + fine-tuning utilities included (`data/*.jsonl`, `load_dataset.py`, `solutions.ipynb`)

## Upcoming (most relevant)

- Conversation memory (store chat history per session and send prior turns to the model)
- Configurable model/system prompt (switch between base and fine-tuned model IDs without editing code)
- Basic safety/guardrails (crisis language detection + clearer “not medical advice” UX)

## What this repo contains

- A Django web app with a simple chat interface (jQuery + AJAX)
- A single view that calls OpenAI and returns JSON
- Dataset artifacts and utilities for fine-tuning experiments

## High-level architecture

Request flow:

1. Browser loads the chat page.
2. User submits a message (AJAX `POST`).
3. Django view calls the OpenAI Chat Completions API.
4. View returns JSON: `{ "reply": "..." }`.
5. Frontend appends the reply to the chat transcript.

Key entrypoints:

- Web handler: `chatbot/views.py` (`chatbot_response`)
- Routing: `chatbot/urls.py` → included by `chatbot_project/urls.py`
- Templates: `chatbot/templates/base.html` and `chatbot/templates/chatbot/chat.html`

## Project layout

- `chatbot_project/`: Django project settings/ASGI/WSGI/URL configuration
- `chatbot/`: Django app (views/urls/templates)
- `data/`: JSONL training/validation files and downloaded dataset assets
- `load_dataset.py`: downloads + stores the Hugging Face dataset locally
- `solutions.ipynb`: step-by-step dataset prep and fine-tuning experiments

## Prerequisites

- Python 3.10+ (this repo’s `.venv/` is typically created with Python 3.12)
- An OpenAI API key (set as `OPENAI_API_KEY`)

## Setup

### 1) Create/activate a virtual environment

If you already have `.venv/`, activate it:

```bash
source .venv/bin/activate
```

Or create one:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

### 2) Install dependencies

This repo doesn’t include a pinned dependency file. Install the minimum set:

```bash
pip install django python-dotenv openai
```

Optional (only needed for dataset/fine-tuning utilities):

```bash
pip install datasets jupyter
```

### 3) Configure environment variables

Create a `.env` file in the repo root:

```bash
OPENAI_API_KEY=your_key_here
```

Notes:

- `.env` is loaded in `chatbot_project/settings.py` via `python-dotenv`.
- Never commit real API keys.

## Run the web app

Start the development server:

```bash
python3 manage.py runserver 0.0.0.0:8080
```

Then open:

- http://localhost:8080/

## How the OpenAI call works

In `chatbot/views.py`:

- The OpenAI client is initialized with `OpenAI(api_key=os.getenv('OPENAI_API_KEY'))`.
- The view sends a single user message to `client.chat.completions.create(...)`.
- The model is currently set to `gpt-4.1-2025-04-14`.

If you switch to a fine-tuned model later, you typically only need to change the `model=...` value.

## Dataset + fine-tuning utilities (optional)

- `load_dataset.py` downloads the Hugging Face dataset `Amod/mental_health_counseling_conversations` and saves it under `data/mental_health_counseling_conversations/`.
- `data/train.jsonl` and `data/validation.jsonl` are example JSONL files formatted for chat fine-tuning.
- `solutions.ipynb` shows a full workflow (sampling, JSONL generation, and fine-tuning job creation).

Important: fine-tuning jobs can fail if any single JSONL example exceeds the model’s context window. Ensure each training line stays within the model’s token limit before uploading.

## Frontend notes

- The UI is implemented in `chatbot/templates/chatbot/chat.html` using jQuery.
- CSRF is handled via `{% csrf_token %}` and sent along with the AJAX POST.

## Template gotcha (common source of errors)

Django template tags must remain intact.

If an auto-formatter splits a tag like this:

```text
{%\nblock content %}
```

Django won’t recognize it, and you may see:

- `TemplateSyntaxError: Invalid block tag ... 'endblock'`

Fix by keeping template tags on a single line, e.g.:

```text
{% block content %}
```

This repo includes workspace settings to reduce formatter damage for templates:

- `.vscode/settings.json`

## Development tips

- If you add models, you’ll also want to add `chatbot` to `INSTALLED_APPS` in `chatbot_project/settings.py` and create migrations.
- The project uses SQLite (`db.sqlite3`) by default.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'django'`**: you’re likely not using the repo’s virtual environment. Activate `.venv/` and reinstall deps.
- **Template `endblock` errors**: see “Template gotcha” above.
- **OpenAI auth errors**: verify `.env` exists and `OPENAI_API_KEY` is set.

## Safety & privacy

This project is for educational/demo use. Do not treat outputs as medical advice. Avoid sending sensitive personal data to third-party APIs.
