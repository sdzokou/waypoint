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