"""
author: David den Uyl (djdenuyl@gmail.com)
date: 2022-10-19
"""
from enum import Enum


class Color(Enum):
    """ represents the options for the player color"""
    BLACK = 'black'
    WHITE = 'white'
    NONE = None


def opponent(color: Color) -> Color:
    """ return the opposing color of the given color"""
    return Color.BLACK if color == Color.WHITE else Color.WHITE
