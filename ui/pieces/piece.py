"""
Abstract UI Piece class

author: David den Uyl (djdenuyl@gmail.com)
date: 2023-03-23
"""
from abc import ABC, abstractmethod
from dash.html import Div
from src.piece import PieceOption
from ui.pieces.builder import UIPieceBuilder
from utils.color import Color
from utils.settings import PIECE_SCALE_FACTOR


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
                '--piece-scale': PIECE_SCALE_FACTOR
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
