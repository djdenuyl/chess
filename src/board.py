from dataclasses import dataclass, field
from itertools import chain
from src.piece import PieceType, Blank, Knight, Pawn
from src.tile import Tile
from typing import Optional, Type, Iterator
from utils.color import Color
from utils.letters import LETTERS
from utils.vector import get_vector


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
    def flat(self) -> Iterator:
        """ return a flattened unnested chain of tiles"""
        return chain(*self.tiles)

    def tile_by_index(self, idx) -> Tile:
        """ return a tile by its index """
        return list(chain(*self.tiles))[idx]

    def tile_by_name(self, name) -> Tile:
        """ return a tile by its name """
        tile, *_ = [t for t in list(chain(*self.tiles)) if t.name == name]
        return tile

    def tiles_by_color(self, color: Color) -> list[Tile]:
        """ return all tiles occupied by a piece of given color"""
        return [t for t in self.flat if t.piece.color == color]

    def tiles_by_piece_type(self, piece_type: Type[PieceType], color: Optional[Color] = None) -> list[Tile]:
        """ return the tiles containing a particular piece, optionally also by its color"""
        if color is None:
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

    def opponent_tiles(self, tile: Tile) -> list[Tile]:
        """ return all the tiles occupied by the opponent of the piece at the given tile. """
        return [
            t for t in self.flat if t.piece.color != tile.piece.color and not isinstance(t.piece, Blank)
        ]

    def tiles_between(self, frm: Tile, to: Tile) -> list[Tile]:
        """ return all the tiles between two tiles. Will only return tiles for on-axis and diagonal comparisons.
        Will return an empty list for knights. """
        # only knights ignore the clear path rule, other pieces obey
        if not isinstance(frm.piece, Knight):
            x_idx = self._horizontal_indices_between(frm, to)
            y_idx = self._vertical_indices_between(frm, to)

            return [self.tiles[self.height - y][x] for x, y in zip(x_idx, y_idx)]

        return []

    @staticmethod
    def _horizontal_indices_between(frm: Tile, to: Tile) -> range:
        """ collect the axis indices horizontally between the frm and to tile"""
        drc, lng = get_vector(frm, to)
        return range(frm.x_int + drc.value[0], to.x_int, drc.value[0] or 1) or [frm.x_int] * (abs(lng.dy) - 1)

    @staticmethod
    def _vertical_indices_between(frm: Tile, to: Tile) -> range:
        """ collect the axis indices vertically between the frm and to tile"""
        drc, lng = get_vector(frm, to)
        return range(frm.y + drc.value[1], to.y, drc.value[1] or 1) or [frm.y] * (abs(lng.dx) - 1)

    def reset_passable_pawns(self, color: Color):
        pawn_tiles = self.tiles_by_piece_type(Pawn, color)
        for p in pawn_tiles:
            if isinstance(p.piece, Pawn):
                self.tiles[self.height - p.y][p.x_int].piece.is_passable = False
