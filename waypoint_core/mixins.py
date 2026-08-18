"""
Mixins and duck-typed helpers for the Waypoint domain engine.

A mixin is not a trail: it carries one narrow behaviour meant to be composed
into a trail class. It never stands alone and never defines __init__ state of
its own beyond what it is given.
"""


class ElevationMixin:
    """
    Adds grade reporting to any class exposing distance and elevation_gain_m.
    """

    def grade_percent(self):
        """
        Average steepness over the whole trail, as a percentage.

        Climb in metres divided by horizontal distance in metres. A flat
        trail returns 0.0 rather than dividing by zero.

        :return: the average grade as a float percentage
        """
        metres = self.distance.convert("km").magnitude * 1000
        if metres == 0:
            return 0.0
        return self.elevation_gain_m / metres * 100

    def steepness_label(self):
        """
        Plain-language reading of the grade.

        :return: one of "flat", "rolling", "steep", "very steep"
        """
        grade = self.grade_percent()
        if grade < 2:
            return "flat"
        if grade < 6:
            return "rolling"
        if grade < 12:
            return "steep"
        return "very steep"


class RatingMixin:
    """
    Adds star ratings to any class, storing them lazily on first use.
    """

    def add_rating(self, stars):
        """
        Record one visitor rating.

        The list is created on first call, so the mixin needs no __init__
        and stays composable with any trail class.

        :param stars: a rating from 1 to 5
        :raises ValueError: if stars is outside 1..5
        :return: None
        """
        if not 1 <= stars <= 5:
            raise ValueError("stars must be between 1 and 5")
        if not hasattr(self, "_ratings"):
            self._ratings = []
        self._ratings.append(int(stars))

    def average_rating(self):
        """
        Mean of the recorded ratings.

        :return: the average as a float, or 0.0 when nothing was rated yet
        """
        ratings = getattr(self, "_ratings", [])
        if not ratings:
            return 0.0
        return sum(ratings) / len(ratings)


class FakeTrail:
    """
    A stand-in for tests, inheriting nothing from the Trail hierarchy.

    It works in the polymorphic loop purely because it exposes the same two
    methods. Python asks whether the object can do the job, not what it is.
    """

    def __init__(self, name, hours):
        """
        Build a fake trail returning a fixed time.

        :param name: the display name
        :param hours: the time this fake always reports
        :return: None
        """
        self.name = name
        self._hours = hours

    def estimated_time(self):
        """
        :return: the fixed time this fake was built with
        """
        return self._hours

    def summary(self):
        """
        :return: a one-line description of the fake
        """
        return f"Fake trail: {self.name} — always {self._hours} h"