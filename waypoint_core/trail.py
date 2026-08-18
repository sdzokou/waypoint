"""
Trail hierarchy for the Waypoint domain engine.

Trail is an abstract base class: it holds the state and rules common to every
trail, but refuses to be instantiated because pacing and gear depend on the
kind of outing. DayHike, BackpackingRoute and TrailRun supply that behaviour.
"""

from abc import ABC, abstractmethod

from waypoint_core.distance import Distance
from waypoint_core.mixins import ElevationMixin, RatingMixin


class Trail(ABC):
    """
    Abstract base for every kind of trail.

    Instance state describes one trail; the class variable default_unit is
    shared platform-wide and is used when incoming data omits a unit.
    Subclasses must supply estimated_time() and summary().
    """

    default_unit = "km"
    ALLOWED_DIFFICULTIES = ("easy", "moderate", "hard", "expert")

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty="easy"):
        """
        Build a Trail, validating every field before storing it.

        :param trail_id: the unique identifier used for equality and de-duplication
        :param name: the display name of the trail
        :param distance: a Distance instance describing the trail length
        :param elevation_gain_m: total climb in metres; must be zero or positive
        :param difficulty: one of ALLOWED_DIFFICULTIES
        :raises TypeError: if distance is not a Distance instance
        :raises ValueError: if elevation or difficulty is invalid
        :return: None
        """
        if not isinstance(distance, Distance):
            raise TypeError("distance must be a Distance instance")
        if not Trail.valid_elevation(elevation_gain_m):
            raise ValueError("elevation_gain_m cannot be negative")

        self.trail_id = trail_id
        self.name = name
        self.distance = distance
        self.elevation_gain_m = int(elevation_gain_m)
        self._difficulty = None
        self.set_difficulty(difficulty)

    @abstractmethod
    def estimated_time(self):
        """
        Estimated moving time for this trail, in hours.

        Abstract: a day hike, a multi-day route and a trail run pace
        differently, so each subclass computes its own figure.

        :return: the estimated time in hours as a float
        """

    @abstractmethod
    def summary(self):
        """
        One-line description tailored to the kind of trail.

        :return: a human-readable string
        """

    def packing_list(self):
        """
        Gear every outing needs, whatever its kind.

        Subclasses extend this list with super() rather than replacing it,
        so the shared essentials are declared in exactly one place.

        :return: a list of gear names
        """
        return ["water", "map", "first-aid kit"]

    def set_difficulty(self, difficulty):
        """
        Mutator: change the difficulty only if it is allowed.

        This is the single door into _difficulty, so the object can never
        hold a value outside ALLOWED_DIFFICULTIES.

        :param difficulty: the requested difficulty
        :raises ValueError: if the difficulty is not in the allowed set
        :return: None
        """
        if not Trail.valid_difficulty(difficulty):
            raise ValueError(
                f"difficulty must be one of {Trail.ALLOWED_DIFFICULTIES}, got {difficulty!r}"
            )
        self._difficulty = difficulty

    def get_difficulty(self):
        """
        Accessor: read the difficulty without exposing the attribute itself.

        :return: the current difficulty as a string
        """
        return self._difficulty

    @staticmethod
    def valid_difficulty(value):
        """
        Pure utility: is this value an acceptable difficulty?

        :param value: the candidate difficulty
        :return: True if the value is allowed, otherwise False
        """
        return value in Trail.ALLOWED_DIFFICULTIES

    @staticmethod
    def valid_elevation(value):
        """
        Pure utility: is this value an acceptable elevation gain?

        :param value: the candidate elevation in metres
        :return: True if the value is numeric and not negative, otherwise False
        """
        return isinstance(value, (int, float)) and value >= 0

    @classmethod
    def from_dict(cls, data):
        """
        Alternate constructor: build a trail from an API-shaped dictionary.

        Called on a concrete subclass, cls is that subclass, so the same code
        builds a DayHike or a TrailRun without any branching.

        :param data: a dict with keys id, name, distance, elevation_gain_m, difficulty
        :raises ValueError: if the underlying data is invalid
        :return: a new instance of whichever subclass was called
        """
        unit = data.get("unit", cls.default_unit)
        distance = Distance(data["distance"], unit)
        return cls(
            trail_id=data["id"],
            name=data["name"],
            distance=distance,
            elevation_gain_m=data.get("elevation_gain_m", 0),
            difficulty=data.get("difficulty", "easy"),
        )

    @classmethod
    def set_default_unit(cls, unit):
        """
        Change the platform-wide default unit for newly created trails.

        :param unit: the new default unit, "km" or "mi"
        :raises ValueError: if the unit is unsupported
        :return: None
        """
        if unit not in Distance.VALID_UNITS:
            raise ValueError(f"unit must be one of {Distance.VALID_UNITS}, got {unit!r}")
        cls.default_unit = unit

    def _naismith_hours(self, flat_speed_kmh, ascent_m_per_hour):
        """
        Naismith-style estimate shared by every subclass.

        Walking time over the ground plus a penalty for the climb. Subclasses
        pass their own pace, so the formula itself is written once.

        :param flat_speed_kmh: horizontal speed in kilometres per hour
        :param ascent_m_per_hour: metres of climb absorbed in one hour
        :return: the estimated time in hours as a float
        """
        km = self.distance.convert("km").magnitude
        return km / flat_speed_kmh + self.elevation_gain_m / ascent_m_per_hour

    def __eq__(self, other):
        """
        Two trails are the same trail when they share a trail_id.

        :param other: the object to compare against
        :return: True if other is a Trail with the same trail_id
        """
        if not isinstance(other, Trail):
            return NotImplemented
        return self.trail_id == other.trail_id

    def __hash__(self):
        """
        Keep Trail usable in sets and dict keys now that __eq__ is defined.

        :return: the hash of the trail_id
        """
        return hash(self.trail_id)

    def __str__(self):
        """
        Human-readable summary line.

        :return: a string such as "Sentier des Chutes (8.00 km, moderate)"
        """
        return f"{self.name} ({self.distance}, {self._difficulty})"

    def __repr__(self):
        """
        Unambiguous form for debugging, naming the concrete subclass.

        :return: a string such as DayHike(id='T1', name='Sentier des Chutes')
        """
        return f"{type(self).__name__}(id={self.trail_id!r}, name={self.name!r})"


class DayHike(Trail):
    """
    A walk done between sunrise and sunset, at a steady hiking pace.
    """

    FLAT_SPEED_KMH = 4.0
    ASCENT_M_PER_HOUR = 600.0

    def estimated_time(self):
        """
        Hiking pace: 4 km/h on the flat, one hour per 600 m of climb.

        :return: the estimated time in hours as a float
        """
        return self._naismith_hours(self.FLAT_SPEED_KMH, self.ASCENT_M_PER_HOUR)

    def summary(self):
        """
        :return: a one-line description of the day hike
        """
        return f"Day hike: {self.name} — {self.distance}, about {self.estimated_time():.1f} h"

    def packing_list(self):
        """
        Extend the shared essentials with day-hike gear.

        :return: a list of gear names
        """
        return super().packing_list() + ["snack", "rain jacket"]


class BackpackingRoute(Trail):
    """
    A multi-day route walked with a full pack, so slower on both ground and climb.
    """

    FLAT_SPEED_KMH = 3.0
    ASCENT_M_PER_HOUR = 400.0

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty="easy", days=2):
        """
        Build a backpacking route, adding the number of days on the trail.

        :param trail_id: the unique identifier
        :param name: the display name
        :param distance: a Distance instance
        :param elevation_gain_m: total climb in metres
        :param difficulty: one of ALLOWED_DIFFICULTIES
        :param days: number of days planned; must be at least 1
        :raises ValueError: if days is less than 1
        :return: None
        """
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)
        if days < 1:
            raise ValueError("days must be at least 1")
        self.days = int(days)

    def estimated_time(self):
        """
        Pack-laden pace: 3 km/h on the flat, one hour per 400 m of climb.

        :return: the total moving time in hours as a float
        """
        return self._naismith_hours(self.FLAT_SPEED_KMH, self.ASCENT_M_PER_HOUR)

    def summary(self):
        """
        :return: a one-line description including the daily walking load
        """
        per_day = self.estimated_time() / self.days
        return (
            f"Backpacking route: {self.name} — {self.distance} over {self.days} days, "
            f"about {per_day:.1f} h per day"
        )

    def packing_list(self):
        """
        Extend the shared essentials with overnight gear.

        :return: a list of gear names
        """
        return super().packing_list() + ["tent", "sleeping bag", "stove"]


class TrailRun(Trail):
    """
    The same ground covered running, so far quicker and less penalised by climb.
    """

    FLAT_SPEED_KMH = 9.0
    ASCENT_M_PER_HOUR = 900.0

    def estimated_time(self):
        """
        Running pace: 9 km/h on the flat, one hour per 900 m of climb.

        :return: the estimated time in hours as a float
        """
        return self._naismith_hours(self.FLAT_SPEED_KMH, self.ASCENT_M_PER_HOUR)

    def summary(self):
        """
        :return: a one-line description of the run
        """
        return f"Trail run: {self.name} — {self.distance}, about {self.estimated_time():.1f} h"

    def packing_list(self):
        """
        Replace the shared essentials rather than extending them.

        A runner carries a flask and gels, not a first-aid kit and a paper
        map. This is the one place where super() is deliberately not called.

        :return: a list of gear names
        """
        return ["soft flask", "energy gels"]


class GuidedDayHike(DayHike):
    """
    A day hike led by a guide, who sets a slightly slower group pace.

    Third level of the hierarchy: Trail -> DayHike -> GuidedDayHike.
    """

    GROUP_SLOWDOWN = 1.15

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty="easy", guide_name="staff"):
        """
        Build a guided day hike, adding the guide leading the group.

        :param trail_id: the unique identifier
        :param name: the display name
        :param distance: a Distance instance
        :param elevation_gain_m: total climb in metres
        :param difficulty: one of ALLOWED_DIFFICULTIES
        :param guide_name: the guide leading the outing
        :return: None
        """
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)
        self.guide_name = guide_name

    def estimated_time(self):
        """
        A guided group moves slower than a solo hiker, so pad the parent figure.

        Extends rather than replaces: the DayHike calculation is reused.

        :return: the estimated time in hours as a float
        """
        return super().estimated_time() * self.GROUP_SLOWDOWN

    def summary(self):
        """
        :return: a one-line description naming the guide
        """
        return f"{super().summary()} — led by {self.guide_name}"


class RatedMountainHike(ElevationMixin, RatingMixin, DayHike):
    """
    A day hike that also reports its grade and collects visitor ratings.

    MRO: RatedMountainHike -> ElevationMixin -> RatingMixin -> DayHike
         -> Trail -> ABC -> object

    Python walks that list left to right, so a name defined in a mixin wins
    over the same name in DayHike. The mixins come first deliberately.
    """

    def summary(self):
        """
        Extend the DayHike summary with grade and rating.

        :return: a one-line description including steepness and stars
        """
        return (
            f"{super().summary()} — {self.steepness_label()} "
            f"({self.grade_percent():.1f}%), rated {self.average_rating():.1f}/5"
        )