import math


def get_directions(start: tuple, stop: tuple) -> tuple:
    """
    Returns the rise and run directions
    from the start to the stop in a tuple
    """
    radians = math.atan2(stop[1] - start[1], stop[0] - start[0])
    return (math.cos(radians), math.sin(radians))


def get_distance(start: tuple, stop: tuple) -> int:
    """
    Returns the distance between two points
    """
    dist = math.hypot(stop[0] - start[0], stop[1] - start[1])
    return int(dist)


def get_angle_to(start: tuple, stop: tuple):
    """
    Returns the angle from start to stop in degrees
    """
    dx = stop[0] - start[0]
    dy = stop[1] - start[1]
    radians = math.atan2(-dy, dx)
    radians %= 2 * math.pi
    return math.degrees(radians)
