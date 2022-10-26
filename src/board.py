from dataclasses import dataclass, field
from itertools import chain
from src.tile import Tile
from utils.letters import LETTERS


@dataclass
class Board:
    height: int = 8
    width: int = 8
    tiles: list[list[Tile]] = field(init=False)

    def __post_init__(self):
        self.__init_board()

    def __init_board(self):
        """ initialize an empty game board """
        self.tiles = [
            [
                Tile(LETTERS[w], self.height - h) for w in range(self.width)
            ] for h in range(self.height)
        ]

    def tile_by_index(self, idx) -> Tile:
        """ return a tile by its index """
        return list(chain(*self.tiles))[idx]

    def tile_by_name(self, name) -> Tile:
        """ return a tile by its name """
        tile, *_ = [t for t in list(chain(*self.tiles)) if t.name == name]
        return tile

    def index_by_name(self, name) -> int:
        """ return a tile index by its name"""
        return [i for i, tile in enumerate(chain(*self.tiles)) if tile.name == name][0]
