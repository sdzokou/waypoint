"""
Itinerary class for the Waypoint domain engine.

An Itinerary is a composition: it HAS-A an ordered list of Trail objects.
It is not a kind of Trail, so composition is used rather than inheritance.
"""

from waypoint_core.distance import Distance
from waypoint_core.trail import Trail


class Itinerary:
    """
    An ordered plan made of trails.

    Each Itinerary owns its own list, so adding a trail to one plan can
    never affect another.
    """

    def __init__(self, name, trails=None):
        """
        Build an Itinerary with its own private list of trails.

        The default is None rather than [] on purpose: a mutable default
        argument would be created once and shared by every Itinerary.

        :param name: the display name of the itinerary
        :param trails: an optional iterable of Trail objects to start from
        :return: None
        """
        self.name = name
        self._trails = list(trails) if trails is not None else []

    @property
    def trails(self):
        """
        Read-only view of the trails, so callers cannot mutate the list.

        :return: a tuple of Trail objects in insertion order
        """
        return tuple(self._trails)

    def add_trail(self, trail):
        """
        Append a trail to this itinerary.

        :param trail: the Trail to add
        :raises TypeError: if the argument is not a Trail
        :return: None
        """
        if not isinstance(trail, Trail):
            raise TypeError("only Trail instances can be added to an itinerary")
        self._trails.append(trail)

    def total_distance(self, unit="km"):
        """
        Sum every trail length, converting each one to a common unit first.

        :param unit: the unit the total should be expressed in
        :raises ValueError: if the unit is unsupported
        :return: a Distance holding the total
        """
        if unit not in Distance.VALID_UNITS:
            raise ValueError(f"unit must be one of {Distance.VALID_UNITS}, got {unit!r}")
        total = 0.0
        for trail in self._trails:
            total += trail.distance.convert(unit).magnitude
        return Distance(total, unit)

    def __len__(self):
        """
        Support len(itinerary).

        :return: the number of trails in the itinerary
        """
        return len(self._trails)

    def __str__(self):
        """
        Human-readable summary.

        :return: a string such as "Weekend Gatineau: 3 trails, 21.40 km"
        """
        return f"{self.name}: {len(self._trails)} trails, {self.total_distance()}"