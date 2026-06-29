# KanMind Backend

A Kanban-style task management API (boards → tasks), built with Django REST Framework.

## Learning focus

This is a learning project. The **primary goal was understanding DRF**, not picking one "correct" style. That is intentionally visible in the code: views are deliberately mixed — function-based and class-based, bare `APIView`, `generics`, and `mixins` side by side. Auth and permissions are implemented in several variants (global vs. per-view permissions, view-level vs. object-level checks). The point was to feel the trade-offs of each approach, not to keep the codebase uniform.

## Tech stack

- Python 3, Django + Django REST Framework
- SQLite (development)
- Token-based authentication

## Project layout

One Django app per domain; API code lives in each app's `api/` subfolder.

```
backend/
├── core/            project config (settings, root urls)
├── user_auth_app/   registration, login, tokens
├── boards_app/      Kanban boards
└── tasks_app/       tasks, comments
```

All endpoints are mounted under `/api/`.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
