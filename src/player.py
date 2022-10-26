"""
Created on %(date)s

@author: David den Uyl (ddenuyl@bebr.nl)
"""
from dataclasses import dataclass
from typing import Type
from src.piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King
from src.tile import Tile, tiles
from utils.color import Color


@dataclass
class Player:
    color: Color
    start_positions: dict[Type[Piece], list[Tile]]


WHITE_PLAYER = Player(
    color=Color.WHITE,
    start_positions={
        Pawn: tiles(['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2']),
        Rook: tiles(['A1', 'H1']),
        Knight: tiles(['B1', 'G1']),
        Bishop: tiles(['C1', 'F1']),
        Queen: tiles(['D1']),
        King: tiles(['E1'])
    }
)

BLACK_PLAYER = Player(
    color=Color.BLACK,
    start_positions={
        Pawn: tiles(['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7']),
        Rook: tiles(['A8', 'H8']),
        Knight: tiles(['B8', 'G8']),
        Bishop: tiles(['C8', 'F8']),
        Queen: tiles(['D8']),
        King: tiles(['E8']),
    }
)
