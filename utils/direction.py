from enum import Enum


class Direction(Enum):
    N = (0, 1)
    NE = (1, 1)
    E = (1, 0)
    SE = (1, -1)
    S = (0, -1)
    SW = (-1, -1)
    W = (-1, 0)
    NW = (-1, 1)
    NONE = (0, 0)


STRAIGHT_DIRECTIONS = (Direction.N, Direction.E, Direction.S, Direction.W)
DIAGONAL_DIRECTIONS = (Direction.NE, Direction.SE, Direction.SW, Direction.NW)
