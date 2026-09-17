# KanMind Backend

REST backend for a Kanban-style task management app. Users register with
e-mail and password, log in with a token, and organise their work as boards
with tasks, assignees, reviewers and comments.

## Stack

- Python 3, Django, Django REST Framework
- Token authentication (`rest_framework.authtoken`)
- SQLite (development)
- django-cors-headers for the separate frontend

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Generate a secret key for `.env`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

For development, `requirements-dev.txt` adds flake8 and autopep8.

## Environment variables

All configuration comes from `.env` (see `.env.example`). `SECRET_KEY` and
`CORS_ALLOWED_ORIGINS` are required; the server refuses to start without them.

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django signing key; generate a fresh one per environment |
| `DEBUG` | `True` for local development only; anything else means off |
| `ALLOWED_HOSTS` | Comma separated host names Django accepts |
| `CORS_ALLOWED_ORIGINS` | Comma separated frontend origins, with scheme and port |

`ALLOWED_HOSTS` names the host this API is reached at, `CORS_ALLOWED_ORIGINS`
the origins a browser may call it from. The two are unrelated checks.

## API

All endpoints live under `/api/`. Authenticated endpoints expect the token
from registration or login:

```
Authorization: Token <token>
```

### Auth

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| POST | `registration/` | no | Create a user and return a token |
| POST | `login/` | no | Check credentials and return a token |
| GET | `email-check/?email=` | yes | Look up a user by e-mail address |

### Boards

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| GET | `boards/` | yes | Boards the user owns or is a member of |
| POST | `boards/` | yes | Create a board; the creator becomes owner and member |
| GET | `boards/<board_id>/` | owner or member | Board with its members and tasks |
| PATCH | `boards/<board_id>/` | owner or member | Update title and members |
| DELETE | `boards/<board_id>/` | owner | Delete the board and its tasks |

### Tasks

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| POST | `tasks/` | board owner or member | Create a task on a board |
| GET | `tasks/assigned-to-me/` | yes | Tasks assigned to the user |
| GET | `tasks/reviewing/` | yes | Tasks the user reviews |
| PATCH | `tasks/<task_id>/` | board member or task owner | Update a task |
| DELETE | `tasks/<task_id>/` | task owner or board owner | Delete a task |
| GET | `tasks/<task_id>/comments/` | board owner or member | Comments of a task |
| POST | `tasks/<task_id>/comments/` | board owner or member | Write a comment |
| DELETE | `tasks/<task_id>/comments/<comment_id>/` | comment author | Delete a comment |

## Concepts

**Permission model.** A task has no members of its own: the board it belongs
to decides who may act. Every board has one `owner` and a `members` list, and
the permission classes derive from those two. Where the board comes from
differs per endpoint, which is why the checks are split into separate classes:
from the URL for board endpoints, from the request payload when a task is
created, and from the task's board for everything else.

**Layered structure.** One Django app per domain (`user_auth_app`,
`boards_app`, `tasks_app`), models at app root, API code in each app's `api/`
subfolder. `core/urls.py` mounts every app's routes under `/api/`.

**Validation in serializers, not views.** Serializers own the shape of the
data, views only orchestrate. Assignee and reviewer are read as nested user
objects and written as ids, so each task serializer carries both a read and a
write field for them.

**Error responses.** Client mistakes answer with 400, 401, 403, 404 or 405.
Input that reaches the code before a serializer runs, such as a query
parameter or the board id inside a task payload, is validated explicitly so
that a malformed request cannot turn into a server error.

## Learning focus

This is a learning project, and understanding DRF mattered more than a uniform
style. The views therefore show several approaches side by side: function-based
views next to `APIView`, `generics` and `mixins`, and permissions both global
and per view, both view-level and object-level. The point was to compare the
trade-offs of each approach in one codebase.

## Project layout

```
core/             settings, root urls, wsgi
user_auth_app/    registration, login, tokens, user profile
boards_app/       Kanban boards
tasks_app/        tasks and comments
<app>/api/        serializers, views, urls and permissions of the REST API
```
