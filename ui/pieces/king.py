"""
UI King class

author: David den Uyl (djdenuyl@gmail.com)
date: 2023-03-23
"""
from dash.html import Div
from ui.pieces.piece import UIPiece
from src.piece import PieceOption


class UIKing(UIPiece):
    @property
    def piece(self) -> PieceOption:
        return PieceOption.KING

    def build_black_piece(self) -> Div:
        return self.builder \
            .add_pedestal() \
            .add_foot() \
            .add_body() \
            .add_body_fill() \
            .add_shoulder() \
            .add_shoulder_hole() \
            .add_shoulder_fill() \
            .add_head() \
            .add_head_hole() \
            .add_head_fill() \
            .add_crown() \
            .add_left_crown_hole() \
            .add_center_crown_hole() \
            .add_right_crown_hole() \
            .add_cross() \
            .build()

    def build_white_piece(self) -> Div:
        return self.builder \
            .add_pedestal() \
            .add_pedestal_hole() \
            .add_foot() \
            .add_foot_hole() \
            .add_body() \
            .add_body_hole() \
            .add_body_fill() \
            .add_shoulder() \
            .add_shoulder_hole() \
            .add_head() \
            .add_head_hole() \
            .add_crown() \
            .add_left_crown_hole() \
            .add_center_crown_hole() \
            .add_right_crown_hole() \
            .add_cross() \
            .build()