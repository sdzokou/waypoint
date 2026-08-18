"""
Distance value type for the Waypoint domain engine.

A Distance holds a magnitude and a unit ("km" or "mi"). It refuses negative
magnitudes at construction time and can produce a converted copy of itself
in the other supported unit.
"""

KM_PER_MILE = 1.609344
MILES_PER_KM = 1 / KM_PER_MILE


class Distance:
    """
    A length expressed in a supported unit.

    The magnitude and the unit are stored privately and exposed through
    read-only properties, so a Distance cannot be corrupted after it is built.
    """

    VALID_UNITS = ("km", "mi")

    def __init__(self, magnitude, unit="km"):
        """
        Build a Distance, rejecting invalid data at the door.

        :param magnitude: the numeric length; must be zero or positive
        :param unit: the unit of measure, either "km" or "mi"
        :raises ValueError: if the unit is unsupported or the magnitude is negative
        :return: None
        """
        if unit not in Distance.VALID_UNITS:
            raise ValueError(f"unit must be one of {Distance.VALID_UNITS}, got {unit!r}")
        if magnitude < 0:
            raise ValueError("distance magnitude cannot be negative")
        self._magnitude = float(magnitude)
        self._unit = unit

    @property
    def magnitude(self):
        """
        Read-only accessor for the stored magnitude.

        :return: the magnitude as a float
        """
        return self._magnitude

    @property
    def unit(self):
        """
        Read-only accessor for the stored unit.

        :return: the unit as a string, "km" or "mi"
        """
        return self._unit

    def convert(self, target_unit):
        """
        Return a NEW Distance expressed in the requested unit.

        The current object is never modified; conversion produces a copy.

        :param target_unit: the unit to convert to, "km" or "mi"
        :raises ValueError: if the target unit is unsupported
        :return: a new Distance in the target unit
        """
        if target_unit not in Distance.VALID_UNITS:
            raise ValueError(f"unit must be one of {Distance.VALID_UNITS}, got {target_unit!r}")
        if target_unit == self._unit:
            return Distance(self._magnitude, self._unit)
        if self._unit == "km":
            return Distance(self._magnitude * MILES_PER_KM, "mi")
        return Distance(self._magnitude * KM_PER_MILE, "km")

    def __str__(self):
        """
        Human-readable form, used by print().

        :return: a string such as "12.50 km"
        """
        return f"{self._magnitude:.2f} {self._unit}"

    def __repr__(self):
        """
        Unambiguous form, used in the debugger and in collections.

        :return: a string such as Distance(12.5, 'km')
        """
        return f"Distance({self._magnitude!r}, {self._unit!r})"
    
    def _as_self_unit(self, other):
        """
        Return other's magnitude expressed in this Distance's unit.

        Shared helper for the arithmetic and comparison operators, so the
        auto-conversion rule lives in exactly one place.

        :param other: the Distance to read
        :return: the magnitude as a float, in self's unit
        """
        return other.convert(self._unit)._magnitude

    def __add__(self, other):
        """
        Add two distances; the result keeps the left operand's unit.

        Mixed units are converted automatically rather than rejected, so a
        total never fails because trails were entered in different units.

        :param other: the Distance to add
        :return: a new Distance, or NotImplemented if other is not a Distance
        """
        if not isinstance(other, Distance):
            return NotImplemented
        return Distance(self._magnitude + self._as_self_unit(other), self._unit)

    def __sub__(self, other):
        """
        Subtract a distance from this one; the result keeps the left unit.

        :param other: the Distance to subtract
        :raises ValueError: if the result would be negative
        :return: a new Distance, or NotImplemented if other is not a Distance
        """
        if not isinstance(other, Distance):
            return NotImplemented
        return Distance(self._magnitude - self._as_self_unit(other), self._unit)

    def __eq__(self, other):
        """
        Compare two distances by physical length, not by stored unit.

        5 km and its exact equivalent in miles are the same length, so they
        compare equal. A small tolerance absorbs floating-point drift.

        :param other: the object to compare against
        :return: True if both represent the same length
        """
        if not isinstance(other, Distance):
            return NotImplemented
        return abs(self._magnitude - self._as_self_unit(other)) < 1e-9

    def __hash__(self):
        """
        Keep Distance hashable after defining __eq__.

        :return: a hash based on the length in kilometres
        """
        return hash(round(self.convert("km")._magnitude, 9))

    def __lt__(self, other):
        """
        Order distances by physical length, so sorted() works on a list.

        :param other: the Distance to compare against
        :return: True if this distance is shorter
        """
        if not isinstance(other, Distance):
            return NotImplemented
        return self._magnitude < self._as_self_unit(other)

    def __gt__(self, other):
        """
        Order distances by physical length.

        :param other: the Distance to compare against
        :return: True if this distance is longer
        """
        if not isinstance(other, Distance):
            return NotImplemented
        return self._magnitude > self._as_self_unit(other)