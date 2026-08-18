"""
View functions for the Waypoint site.

Each view takes an HttpRequest and returns an HttpResponse, usually by
rendering a template with a context dictionary.
"""

from django.shortcuts import render


def home(request):
    """
    Render the landing page.

    :param request: the incoming HttpRequest
    :return: the rendered home page
    """
    context = {
        "site_name": "Waypoint",
        "visitor": "hiker",
        "tagline": "Find a trail, plan the day.",
    }
    return render(request, "home.html", context)


def report(request):
    """
    Show a blank trail-report form, or thank the reporter after a POST.

    GET renders the empty form. POST reads the submitted fields and renders
    a thank-you page greeting the reporter by name. Django rejects any POST
    without a valid CSRF token before this function is ever reached.

    :param request: the incoming HttpRequest
    :return: the form page on GET, the thank-you page on POST
    """
    if request.method == "POST":
        context = {
            "name": request.POST.get("name", "").strip() or "friend",
            "email": request.POST.get("email", "").strip(),
            "trail": request.POST.get("trail", "").strip(),
            "note": request.POST.get("note", "").strip(),
        }
        return render(request, "thanks.html", context)
    return render(request, "report.html")


def search(request):
    """
    Search trails by name fragment.

    The query is read with a default of "", so loading /search with no query
    string renders an empty result page instead of raising a KeyError.

    :param request: the incoming HttpRequest
    :return: the rendered search page
    """
    query = request.GET.get("q", "").strip()
    catalogue = [
        "Sentier des Chutes",
        "Boucle du Lac",
        "La Traversee",
        "Cap Rouge",
        "Mont Tremblant",
    ]
    matches = [name for name in catalogue if query.lower() in name.lower()] if query else []
    context = {
        "query": query,
        "matches": matches,
        "searched": bool(query),
    }
    return render(request, "search.html", context)


def catalog(request):
    """
    Render the public trail catalog from a hardcoded list of trail dicts.

    The data lives in the view for now; Part 6 replaces it with a database
    query without changing the template.

    :param request: the incoming HttpRequest
    :return: the rendered catalog page
    """
    trails = [
        {"name": "Sentier des Chutes", "distance_km": 8.4, "elevation_gain": 320,
         "difficulty": "moderate", "is_open": True},
        {"name": "Boucle du Lac", "distance_km": 4.15, "elevation_gain": 90,
         "difficulty": "easy", "is_open": True},
        {"name": "La Traversee", "distance_km": 21.75, "elevation_gain": 1180,
         "difficulty": "expert", "is_open": True},
        {"name": "Cap Rouge", "distance_km": 12.6, "elevation_gain": 540,
         "difficulty": "hard", "is_open": False},
        {"name": "Mont Tremblant", "distance_km": 16.32, "elevation_gain": 875,
         "difficulty": "expert", "is_open": False},
        {"name": "Chemin du Moulin", "distance_km": 6.05, "elevation_gain": 145,
         "difficulty": "easy", "is_open": True},
    ]
    context = {
        "site_name": "Waypoint",
        "trails": trails,
    }
    return render(request, "catalog.html", context)