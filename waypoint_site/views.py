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