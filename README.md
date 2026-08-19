# Waypoint

A trail-finder and trip-planner built with Python and Django.
Individual term project — CCGC-5003, Summer 2026.

## Project layout

- `waypoint_core/` — the pure-Python domain engine (trails, distances, itineraries)
- `waypoint_site/` — Django project configuration
- `trails/` — Django app holding the Trail model, admin and catalog view

## Setup

    python -m venv env
    env\Scripts\activate
    pip install -r requirements.txt

## Run

    python manage.py migrate
    python manage.py runserver 8010

Then open http://127.0.0.1:8010/

Note: port 8000 is unavailable on the development machine (reserved by
Windows), so the project runs on 8010. Any free port works.

## Admin

Create an administrator account to manage trails:

    python manage.py createsuperuser

Then sign in at http://127.0.0.1:8010/admin/ — adding a trail there makes it
appear on the public catalog at /trails/ with no code change. Closed trails are
excluded from the catalog by the query itself.

## Requirements

Python 3.14 with Django 6.1 (see `requirements.txt`). Django 4.2 is not
compatible with Python 3.14 — the admin raises an AttributeError while
rendering its template context — so the project was upgraded during Part 6.

## Releases

| Tag | Part |
|-----|------|
| v7  | Domain model — classes & objects |
| v8  | Domain model — inheritance, polymorphism & operators |
| v9  | Django project setup |
| v10 | Django — views, URLs & the report form |
| v11 | Django — the trail catalog |
| v12 | Django — the database, models & admin |