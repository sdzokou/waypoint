"""
Admin registration for the trails app.

Registering the Trail model gives staff users a full create/read/update/delete
interface at /admin without writing any views, forms or templates.
"""

from django.contrib import admin

from trails.models import Trail


@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    """
    Control how trails are listed and searched in the admin site.
    """

    list_display = ("name", "distance_km", "elevation_gain", "difficulty", "is_open", "added")
    search_fields = ("name",)
    list_filter = ("difficulty", "is_open")