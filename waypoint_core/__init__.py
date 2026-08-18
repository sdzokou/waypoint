"""
Waypoint domain engine.

Pure-Python core: the classes and rules that describe trails, distances and
itineraries, independent of any web framework.
"""

from waypoint_core.distance import Distance
from waypoint_core.trail import Trail
from waypoint_core.itinerary import Itinerary

__all__ = ["Distance", "Trail", "Itinerary"]