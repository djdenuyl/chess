"""
Created on %(date)s

@author: David den Uyl (ddenuyl@bebr.nl)
"""
from dataclasses import dataclass
from src.piece_option import PieceOption
from src.tile import Tile, tiles
from utils.color import Color


@dataclass
class Player:
    color: Color
    start_positions: dict[PieceOption, list[Tile]]


WHITE_PLAYER = Player(
    color=Color.WHITE,
    start_positions={
        PieceOption.PAWN: tiles(['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2']),
        PieceOption.ROOK: tiles(['A1', 'H1']),
        PieceOption.KNIGHT: tiles(['B1', 'G1']),
        PieceOption.BISHOP: tiles(['C1', 'F1']),
        PieceOption.KING: tiles(['D1']),
        PieceOption.QUEEN: tiles(['E1'])
    }
)

BLACK_PLAYER = Player(
    color=Color.BLACK,
    start_positions={
        PieceOption.PAWN: tiles(['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7']),
        PieceOption.ROOK: tiles(['A8', 'H8']),
        PieceOption.KNIGHT: tiles(['B8', 'G8']),
        PieceOption.BISHOP: tiles(['C8', 'F8']),
        PieceOption.KING: tiles(['D8']),
        PieceOption.QUEEN: tiles(['E8'])
    }
)
