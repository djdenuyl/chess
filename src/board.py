from dataclasses import dataclass, field
from itertools import chain
from src.piece import PieceType, Blank
from src.tile import Tile
from typing import Optional, Type
from utils.color import Color
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

    @property
    def flat(self):
        return chain(*self.tiles)

    def tile_by_index(self, idx) -> Tile:
        """ return a tile by its index """
        return list(chain(*self.tiles))[idx]

    def tile_by_name(self, name) -> Tile:
        """ return a tile by its name """
        tile, *_ = [t for t in list(chain(*self.tiles)) if t.name == name]
        return tile

    def tiles_by_piece_type(self, piece_type: Type[PieceType], color: Optional[Color] = None) -> Optional[list[Tile]]:
        """ return the tiles containing a particular piece, optionally also by its color"""
        if color is not None:
            return [t for t in self.flat if isinstance(t.piece, piece_type)]

        return [t for t in self.flat if isinstance(t.piece, piece_type) and t.piece.color == color]

    def index_by_name(self, name) -> int:
        """ return a tile index by its name"""
        return [i for i, tile in enumerate(chain(*self.tiles)) if tile.name == name][0]

    def surrounding_tiles(self, tile: Tile):
        """ return the tiles surrounding the given tile """
        surrounding_tiles = []
        for t in self.flat:
            if t.x_int - tile.x_int in (-1, 0, 1) \
                    and t.y - tile.y in (-1, 0, 1) \
                    and t != tile:
                surrounding_tiles.append(t)

        return surrounding_tiles

    def opponent_tiles(self, tile: Tile):
        """ return all the tiles occupied by the opponent of the piece at the given tile. """
        return [
            t for t in self.flat if t.piece.color != tile.piece.color and not isinstance(t.piece, Blank)
        ]
