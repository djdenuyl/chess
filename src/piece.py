"""
author: David den Uyl (djdenuyl@gmail.com)
date: 2022-10-19
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar
from utils.color import Color, opponent
from utils.direction import Direction, DIAGONAL_DIRECTIONS, STRAIGHT_DIRECTIONS
from utils.length import Length
from utils.vector import get_vector


class Piece(ABC):
    """ a piece on the board """

    def __init__(self, color: Color):
        self.color = color
        self.has_moved = False

    def __str__(self):
        return self.symbol.get(self.color)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.color}, {self.symbol.get(self.color)})'

    @property
    @abstractmethod
    def symbol(self) -> dict[Color, str]:
        """ a property containing the symbology for the piece. used to return the str repr for the piece"""

    @abstractmethod
    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:  # noqa
        """ this method implements whether movement of Tile frm to Tile to is allowed for the piece"""


class Pawn(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.is_passable = False

    @property
    def symbol(self):
        return {Color.BLACK: '♟', Color.WHITE: '♙'}

    def is_valid_diagonal_move(self, direction: Direction, length: Length) -> bool:
        if abs(length.dx) == 1 and abs(length.dy) == 1:
            if self.color == Color.BLACK and direction in (Direction.SE, Direction.SW) \
                    or self.color == Color.WHITE and direction in (Direction.NE, Direction.NW):
                return True

        return False

    def is_valid_orthogonal_move(self, direction: Direction, length: Length) -> bool:
        if length.size == 1 or (length.size == 2 and not self.has_moved):
            if self.color == Color.BLACK and direction == Direction.S \
                    or self.color == Color.WHITE and direction == Direction.N:
                return True

        return False

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:  # noqa
        direction, length = get_vector(frm, to)
        # regular move / start move
        if self.is_valid_orthogonal_move(direction, length) \
                and isinstance(to.piece, Blank):
            if length.size == 2:
                self.is_passable = True
            return True

        # taking another piece
        if self.is_valid_diagonal_move(direction, length) \
                and to.piece.color == opponent(self.color):
            return True

        return False


PieceType = TypeVar('PieceType', bound=Piece)


class Rook(Piece):
    @property
    def symbol(self):
        return {Color.BLACK: '♜', Color.WHITE: '♖'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:  # noqa
        direction, _ = get_vector(frm, to)

        if direction in STRAIGHT_DIRECTIONS \
                and to.piece.color != self.color:
            return True

        return False


class Knight(Piece):
    @property
    def symbol(self):
        return {Color.BLACK: '♞', Color.WHITE: '♘'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:  # noqa
        direction, length = get_vector(frm, to)

        if direction in DIAGONAL_DIRECTIONS \
                and abs(length.dx) + abs(length.dy) == 3 \
                and to.piece.color != self.color:
            return True

        return False


class Bishop(Piece):
    @property
    def symbol(self):
        return {Color.BLACK: '♝', Color.WHITE: '♗'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:  # noqa
        direction, length = get_vector(frm, to)

        if direction in DIAGONAL_DIRECTIONS \
                and abs(length.dx) == abs(length.dy) \
                and to.piece.color != self.color:
            return True

        return False


class Queen(Piece):
    @property
    def symbol(self):
        return {Color.BLACK: '♛', Color.WHITE: '♕'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:  # noqa
        direction, length = get_vector(frm, to)

        if ((direction in DIAGONAL_DIRECTIONS and abs(length.dx) == abs(length.dy))
            or direction in STRAIGHT_DIRECTIONS) \
                and to.piece.color != self.color:
            return True

        return False


class King(Piece):
    @property
    def symbol(self):
        return {Color.BLACK: '♚', Color.WHITE: '♔'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:  # noqa
        direction, length = get_vector(frm, to)

        if ((direction in DIAGONAL_DIRECTIONS and abs(length.dx) == abs(length.dy))
            or direction in STRAIGHT_DIRECTIONS) \
                and abs(length.dx) <= 1 and abs(length.dy) <= 1 \
                and to.piece.color != self.color:
            return True

        return False


class Blank(Piece):
    """ A placeholder class for tiles unoccupied by pieces"""

    def __init__(self):
        self.color = Color.NONE
        super().__init__(self.color)

    @property
    def symbol(self):
        return {Color.NONE: ''}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:  # noqa
        """ never move a blank field"""
        return False


PIECE_TYPE_MAPPER = {
    'king': King,
    'queen': Queen,
    'bishop': Bishop,
    'knight': Knight,
    'rook': Rook,
    'pawn': Pawn
}


class PieceOption(Enum):
    KING = 'king'
    QUEEN = 'queen'
    BISHOP = 'bishop'
    KNIGHT = 'knight'
    ROOK = 'rook'
    PAWN = 'pawn'
