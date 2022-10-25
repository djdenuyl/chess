# """
# Created on 2022-10-19
# @author: David den Uyl (djdenuyl@gmail.com)
# """
from abc import ABC, abstractmethod
# from enum import Enum
# from lib.player import Color
#
#
# class PieceOption(Enum):
#     PAWN = {Color.BLACK: '♙', Color.WHITE: '♟'}
#     ROOK = {Color.BLACK: '♖', Color.WHITE: '♜'}
#     KNIGHT = {Color.BLACK: '♘', Color.WHITE: '♞'}
#     BISHOP = {Color.BLACK: '♗', Color.WHITE: '♝'}
#     KING = {Color.BLACK: '♔', Color.WHITE: '♚'}
#     QUEEN = {Color.BLACK: '♕', Color.WHITE: '♛'}


class Piece(ABC):
    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def take(self):
        pass


class Pawn(Piece):
    def move(self):
        pass

    def take(self):
        pass
