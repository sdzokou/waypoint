"""
Root URL configuration for the Waypoint site.

Maps each public path to the view that answers it. Every route is named, so
templates can build links with {% url %} instead of hardcoding paths.
"""

from django.contrib import admin
from django.urls import path

from waypoint_site import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("report/", views.report, name="report"),
    path("search/", views.search, name="search"),
    path("catalog/", views.catalog, name="catalog"),
]