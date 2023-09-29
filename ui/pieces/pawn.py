"""
UI Pawn class

author: David den Uyl (djdenuyl@gmail.com)
date: 2023-03-23
"""
from dash.html import Div
from dash_svg import Svg
from parsers.svg import SVGParser
from pathlib import Path
from ui.pieces.piece import UIPiece
from src.piece import PieceOption


class UIPawn(UIPiece):
    @property
    def piece(self) -> PieceOption:
        return PieceOption.PAWN

    def build_black_piece(self) -> Svg:
        return SVGParser.from_file(
            file=Path('assets', 'pieces', 'black', 'pawn.svg'),
            fill='white',
            stroke='black',
            stroke_width=0
        ).parse_svg()

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
            .build()
