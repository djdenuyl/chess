from enum import Enum, auto


class Color(Enum):
    BLACK = auto()
    WHITE = auto()
    NONE = auto()


def opponent(color: Color) -> Color:
    """ return the opposing color of the given color"""
    return Color.BLACK if color == Color.WHITE else Color.WHITE
