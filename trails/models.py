"""
Database models for the trails app.

The Trail model is the persistent counterpart of the pure-Python Trail class
built in Part 1: the same entity, now stored in the database and editable
through the Django admin.
"""

from django.db import models


class Trail(models.Model):
    """
    A hiking trail listed in the public catalog.

    Each field maps to a database column. Django adds an auto-incrementing
    integer primary key named id unless one is declared explicitly.
    """

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("moderate", "Moderate"),
        ("hard", "Hard"),
        ("expert", "Expert"),
    ]

    name = models.CharField(max_length=120)
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    elevation_gain = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    is_open = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return the readable label used by the admin and by shell output.

        :return: the trail name
        """
        return self.name