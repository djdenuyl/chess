"""
UI Knight class

author: David den Uyl (djdenuyl@gmail.com)
date: 2023-03-23
"""
from dash.html import Div
from ui.pieces.piece import UIPiece
from src.piece import PieceOption


class UIKnight(UIPiece):
    @property
    def piece(self) -> PieceOption:
        return PieceOption.KNIGHT

    def build_black_piece(self) -> Div:
        return self.builder \
            .add_pedestal() \
            .add_foot() \
            .add_body() \
            .add_body_fill() \
            .add_right_ear() \
            .add_mane() \
            .add_mane_hole() \
            .add_neck() \
            .add_neck_hole() \
            .add_upper_body() \
            .add_upper_body_fill() \
            .add_snout() \
            .add_nose() \
            .add_nostril() \
            .add_face() \
            .add_left_ear() \
            .add_eye() \
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
            .add_right_ear() \
            .add_mane() \
            .add_mane_hole() \
            .add_neck() \
            .add_neck_hole() \
            .add_snout_outline() \
            .add_snout() \
            .add_nose() \
            .add_nose_hole() \
            .add_face() \
            .add_face_hole() \
            .add_snout_hole() \
            .add_nostril() \
            .add_left_ear() \
            .add_upper_body() \
            .add_upper_body_hole() \
            .add_upper_body_fill() \
            .add_eye_outline() \
            .add_eye() \
            .build()
