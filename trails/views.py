"""
Views for the trails app.

The catalog now reads from the database instead of a hardcoded list, so an
admin can publish or close a trail without any code change.
"""

from django.shortcuts import render

from trails.models import Trail


def catalog(request):
    """
    List the open trails, ordered by distance.

    Closed trails are excluded by the query itself rather than by the
    template, so they can never leak onto the public page.

    :param request: the incoming HttpRequest
    :return: the rendered catalog page
    """
    trails = Trail.objects.filter(is_open=True).order_by("distance_km")
    context = {
        "site_name": "Waypoint",
        "trails": trails,
    }
    return render(request, "catalog.html", context)