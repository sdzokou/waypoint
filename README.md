# Waypoint

A trail-finder and trip-planner built with Python and Django.
Individual term project — CCGC-5003, Summer 2026.

## Project layout

- `waypoint_core/` — the pure-Python domain engine (trails, distances, itineraries)
- `waypoint/` — Django project configuration
- `catalog/` — Django app serving the trail catalog

## Setup

    python -m venv env
    env\Scripts\activate
    pip install -r requirements.txt

## Run

    python manage.py migrate
    python manage.py runserver

Then open http://127.0.0.1:8000/

## Releases

| Tag | Part |
|-----|------|
| v7  | Domain model — classes & objects |