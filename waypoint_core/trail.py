"""
Trail class for the Waypoint domain engine.

A Trail bundles the data describing a hiking trail together with the rules
that keep that data valid: difficulty is checked against an allowed set,
elevation gain cannot be negative, and equality is based on the trail id.
"""

from waypoint_core.distance import Distance


class Trail:
    """
    A single hiking trail.

    Instance state describes one trail; the class variable default_unit is
    shared platform-wide and is used when incoming data omits a unit.
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
        Alternate constructor: build a Trail from an API-shaped dictionary.

        When the dictionary omits a unit, the platform default_unit is used,
        so changing that class variable affects trails created afterwards.

        :param data: a dict with keys id, name, distance, elevation_gain_m, difficulty
        :raises ValueError: if the underlying data is invalid
        :return: a new Trail instance
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

    def __eq__(self, other):
        """
        Two trails are the same trail when they share a trail_id.

        This lets an import de-duplicate records that differ in wording
        but describe the same physical trail.

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
        Unambiguous form for debugging.

        :return: a string such as Trail(id='T1', name='Sentier des Chutes')
        """
        return f"Trail(id={self.trail_id!r}, name={self.name!r})"