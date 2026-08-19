"""
URL configuration for the trails app.

Mounted under /trails/ by the project's root URLconf with include().
"""

from django.urls import path

from trails import views

urlpatterns = [
    path("", views.catalog, name="catalog"),
]