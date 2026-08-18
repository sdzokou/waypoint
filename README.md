# Waypoint

A trail-finder and trip-planner built with Python and Django.
Individual term project — CCGC-5003, Summer 2026.

## Project layout

- `waypoint_core/` — the pure-Python domain engine (trails, distances, itineraries)
- `waypoint_site/` — Django project configuration

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

## Releases

| Tag | Part |
|-----|------|
| v7  | Domain model — classes & objects |
| v9  | Django project setup |