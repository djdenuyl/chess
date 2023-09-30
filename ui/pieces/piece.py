"""
Abstract UI Piece class

author: David den Uyl (djdenuyl@gmail.com)
date: 2023-03-23
"""
from abc import ABC, abstractmethod
from pathlib import Path
from dash.html import Div
from dash_svg import Svg
from parsers.svg import SVGParser
from src.piece import PieceOption, PIECE_TYPE_MAPPER
from src.tile import Tile
from ui.pieces.builder import UIPieceBuilder
from utils.color import Color


def get_piece(tile: Tile) -> Svg | None:
    piece_type = PIECE_TYPE_MAPPER.reverse.get(tile.piece.__class__)

    if piece_type is None:
        return None

    color = tile.piece.color.value

    return SVGParser \
        .from_file(
            file=Path('assets', 'pieces', color, f'pawn.svg'),
            fill='#264653',
            stroke_width=0
        ) \
        .parse_svg(
            with_color=False,
            classes=['piece']
        )


class UIPiece(ABC, Div):
    def __init__(self, color: Color, piece_color: str, bg_color: str, **kwargs):
        self.color = color
        self.bg_color = bg_color
        self.builder = UIPieceBuilder()
        self.className = f'container {self.piece.value} {self.color.value}'
        super().__init__(
            className=self.className,
            style={
                '--piece-color': piece_color,  # TODO: move all settings to settings.py?
                '--bgcolor': bg_color,
            },
            children=self.build_piece(),
            **kwargs
        )

    @property
    @abstractmethod
    def piece(self) -> PieceOption:
        ...

    def build_piece(self) -> Div:
        if self.color == Color.WHITE:
            return self.build_white_piece()

        return self.build_black_piece()

    @abstractmethod
    def build_black_piece(self) -> Div:
        ...

    @abstractmethod
    def build_white_piece(self) -> Div:
        ...
