"""
Created on 2022-10-19
@author: David den Uyl (djdenuyl@gmail.com)
"""
from abc import ABC, abstractmethod
from utils.color import Color
from utils.direction import Direction
from utils.length import Length


class Piece(ABC):
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

    @staticmethod
    def get_vector(frm: 'Tile', to: 'Tile') -> tuple[Direction, Length]:
        """ get the vector containing the direction and length of the movement of the piece"""
        x = -1 if (dx := to.x_int - frm.x_int) < 0 else 1 if dx > 0 else 0
        y = -1 if (dy := to.y - frm.y) < 0 else 1 if dy > 0 else 0

        return Direction((x, y)), Length(dx, dy)


class Pawn(Piece):
    @property
    def symbol(self):
        return {Color.BLACK: '♟', Color.WHITE: '♙'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        direction, length = self.get_vector(frm, to)

        if length.size == 1:
            if self.color == Color.BLACK and direction == Direction.S:
                return True
            elif self.color == Color.WHITE and direction == Direction.N:
                return True

        return False


class Rook(Piece):
    @property
    def symbol(self):
        return {Color.BLACK: '♜', Color.WHITE: '♖'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        return True


class Knight(Piece):
    @property
    def symbol(self):
        return {Color.BLACK: '♞', Color.WHITE: '♘'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        return True


class Bishop(Piece):
    @property
    def symbol(self):
        return {Color.BLACK: '♝', Color.WHITE: '♗'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        return True


class Queen(Piece):
    @property
    def symbol(self):
        return {Color.BLACK:  '♛', Color.WHITE: '♕'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        return True


class King(Piece):
    @property
    def symbol(self):
        return {Color.BLACK:  '♚', Color.WHITE: '♔'}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        return True


class Blank(Piece):
    def __init__(self):
        self.color = Color.NONE
        super().__init__(self.color)

    @property
    def symbol(self):
        return {Color.NONE:  ''}

    def is_valid_move(self, frm: 'Tile', to: 'Tile') -> bool:
        return False


if __name__ == '__main__':
    p = Pawn(Color.BLACK)

    print(p.__repr__())
