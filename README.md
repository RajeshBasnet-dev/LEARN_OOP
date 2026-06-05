# OOP Practice Lab

OOP Practice Lab is a production-ready MVP Django application for practicing Object-Oriented Programming in Python. Students solve structured exercises in a Monaco editor and receive safe AST-only feedback about classes, inheritance, methods, encapsulation, `super()`, and `@property` usage.

## Features

- Django 4 + Django REST Framework backend.
- Custom `UserProfile` model with completed exercise tracking.
- Public exercise catalog and detail API endpoints.
- Authenticated code submission API that evaluates source using Python's `ast` module only.
- Monaco Editor loaded from a CDN for a lightweight vanilla JavaScript frontend.
- Dashboard API and page with aggregate stats and per-concept progress.
- Fixture with exactly three sample exercises: Employee, Manager, and Shape Polymorphism.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd oop_practice_lab
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/exercises.json
python manage.py createsuperuser
python manage.py runserver
```

Visit <http://127.0.0.1:8000/> to start practicing.

## Environment Variables

Create a `.env` file in `oop_practice_lab/` or export these variables:

```bash
SECRET_KEY=replace-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

For PostgreSQL, set `DB_ENGINE=django.db.backends.postgresql` and provide `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`.

## API Endpoints

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/exercises/`
- `GET /api/exercises/<id>/`
- `POST /api/submissions/`
- `GET /api/submissions/`
- `GET /api/submissions/<id>/`
- `GET /api/dashboard/`

## Safety Notes

The evaluator parses submitted code into an AST and performs structural checks. It does not run student code, so submissions are inspected without dynamic execution.
