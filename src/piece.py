"""
Created on 2022-10-19
@author: David den Uyl (djdenuyl@gmail.com)
"""
from abc import ABC, abstractmethod
from utils.color import Color
from utils.direction import Direction, DIAGONAL_DIRECTIONS, STRAIGHT_DIRECTIONS
from utils.start_positions import BLACK_PAWN_START_POSITIONS, WHITE_PAWN_START_POSITIONS
from utils.vector import get_vector


class Piece(ABC):
    """ a piece on the board """
    def __init__(self, color: Color):
        self.color = color

    def __str__(self):
        return self.symbol.get(self.color)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.color}, {self.symbol.get(self.color)})'

    @property
    @abstractmethod
    def symbol(self) -> dict[Color, str]:
        """ a property containing the symbology for the piece. used to return the str repr for the piece"""

    @abstractmethod
    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        """ this method implements whether movement of Tile frm to Tile to is allowed for the piece"""


class Pawn(Piece):
    @property
    def symbol(self):
        return {Color.BLACK: '♟', Color.WHITE: '♙'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        direction, length = get_vector(frm, to)

        # regular move
        if length.size == 1:
            if self.color == Color.BLACK and direction == Direction.S \
                    or self.color == Color.WHITE and direction == Direction.N:
                return True

        # start move
        if length.size == 2:
            # TODO: frm.name in PAWN_START_POSITIONS should really be a check on tiles instead of strings
            # TODO: but importing anything from the tiles module here results in a circular import
            if (self.color == Color.BLACK
                and direction == Direction.S
                and frm.name in BLACK_PAWN_START_POSITIONS) \
                    or (self.color == Color.WHITE
                        and direction == Direction.N
                        and frm.name) in WHITE_PAWN_START_POSITIONS:
                return True

        # taking another piece
        if abs(length.dx) == 1 and abs(length.dy) == 1:
            if self.color == Color.BLACK and direction in (Direction.SE, Direction.SW) \
                    or self.color == Color.WHITE and direction in (Direction.NE, Direction.NW):
                if not isinstance(to.piece, Blank):
                    return True

        return False


class Rook(Piece):
    @property
    def symbol(self):
        return {Color.BLACK: '♜', Color.WHITE: '♖'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        direction, _ = get_vector(frm, to)

        if direction in STRAIGHT_DIRECTIONS \
                and to.piece.color != self.color:
            return True

        return False


class Knight(Piece):
    @property
    def symbol(self):
        return {Color.BLACK: '♞', Color.WHITE: '♘'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        direction, length = get_vector(frm, to)

        if direction in DIAGONAL_DIRECTIONS\
                and abs(length.dx) + abs(length.dy) == 3:
            return True

        return False


class Bishop(Piece):
    @property
    def symbol(self):
        return {Color.BLACK: '♝', Color.WHITE: '♗'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        direction, length = get_vector(frm, to)

        if direction in DIAGONAL_DIRECTIONS \
                and abs(length.dx) == abs(length.dy):
            return True

        return False


class Queen(Piece):
    @property
    def symbol(self):
        return {Color.BLACK:  '♛', Color.WHITE: '♕'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        direction, length = get_vector(frm, to)

        if (direction in DIAGONAL_DIRECTIONS and abs(length.dx) == abs(length.dy)) \
                or direction in STRAIGHT_DIRECTIONS:
            return True

        return False


class King(Piece):
    @property
    def symbol(self):
        return {Color.BLACK:  '♚', Color.WHITE: '♔'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        direction, length = get_vector(frm, to)

        if ((direction in DIAGONAL_DIRECTIONS and abs(length.dx) == abs(length.dy))
                or direction in STRAIGHT_DIRECTIONS) \
                and abs(length.dx) <= 1 and abs(length.dy) <= 1:
            return True

        return False


class Blank(Piece):
    """ A placeholder class for tiles unoccupied by pieces"""
    def __init__(self):
        self.color = Color.NONE
        super().__init__(self.color)

    @property
    def symbol(self):
        return {Color.NONE:  ''}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        """ never move a blank field"""
        return False


if __name__ == '__main__':
    p = Pawn(Color.BLACK)

    print(p.__repr__())
