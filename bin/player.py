"""
Created on %(date)s

@author: David den Uyl (ddenuyl@bebr.nl)
"""
from dataclasses import dataclass
from enum import Enum, auto


class Color(Enum):
    BLACK = auto()
    WHITE = auto()


class PieceOption(Enum):
    PAWN = {Color.BLACK: '♙', Color.WHITE: '♟'}
    ROOK = {Color.BLACK: '♖', Color.WHITE: '♜'}
    KNIGHT = {Color.BLACK: '♘', Color.WHITE: '♞'}
    BISHOP = {Color.BLACK: '♗', Color.WHITE: '♝'}
    KING = {Color.BLACK: '♔', Color.WHITE: '♚'}
    QUEEN = {Color.BLACK: '♕', Color.WHITE: '♛'}


@dataclass
class Player:
    color: Color
    start_positions: dict[PieceOption, list[str]]


WHITE_PLAYER = Player(
    color=Color.WHITE,
    start_positions={
        PieceOption.PAWN: ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2'],
        PieceOption.ROOK: ['A1', 'H1'],
        PieceOption.KNIGHT: ['B1', 'G1'],
        PieceOption.BISHOP: ['C1', 'F1'],
        PieceOption.KING: ['D1'],
        PieceOption.QUEEN: ['E1']
    }
)

BLACK_PLAYER = Player(
    color=Color.BLACK,
    start_positions={
        PieceOption.PAWN: ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7'],
        PieceOption.ROOK: ['A8', 'H8'],
        PieceOption.KNIGHT: ['B8', 'G8'],
        PieceOption.BISHOP: ['C8', 'F8'],
        PieceOption.KING: ['D8'],
        PieceOption.QUEEN: ['E8']
    }
)
