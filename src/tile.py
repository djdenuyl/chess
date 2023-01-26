"""
author: David den Uyl (djdenuyl@gmail.com)
date: 2022-10-19
"""
from dataclasses import dataclass, field
from src.piece import Blank, PieceType
from typing import Optional, Type
from utils.letters import LETTERS


@dataclass
class Tile:
    x: str = field(repr=False)
    y: int = field(repr=False)
    x_int: int = field(init=False, repr=False)
    name: str = field(init=False)
    color: str = field(init=False)
    piece: Optional[Type[PieceType]] = Blank()

    def __set_x_int(self):
        self.x_int = LETTERS.index(self.x)

    def __set_name(self):
        self.name = f'{self.x}{self.y}'

    def __set_color(self):
        # if the sum of the x and the y index is even, the tile is a black tile
        if (self.x_int + self.y) % 2 == 0:
            self.color = '⬜'
        else:
            self.color = '⬛'

    def __post_init__(self):
        self.__set_x_int()
        self.__set_name()
        self.__set_color()

    def __hash__(self):
        return hash((self.name, self.color, self.piece))


def tiles(names: list) -> list[Tile]:
    """ return a list of tiles given a list of tile names """
    return [Tile(x, int(y)) for x, y in names]
