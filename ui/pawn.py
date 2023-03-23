"""
UI elements of the pawn piece

author: David den Uyl (djdenuyl@gmail.com)
date: 2023-03-23
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dash.html import Div
from typing import Optional
from src.piece import PieceOption
from utils.color import Color


class UIPieceBuilder:
    def __init__(self, piece: PieceOption, color: Color, parts: Optional[list] = None):
        self.piece = piece
        self.color = color
        self.parts = parts

        if self.parts is None:
            self.parts = []

    def build(self) -> Div:
        return Div(
            className=f'container {self.piece.value} {self.color.value}',
            children=Div(
                className='model',
                children=self.parts
            )
        )

    def add(self, class_name: str) -> UIPieceBuilder:
        return type(self)(self.piece, self.color, self.parts + [Div(className=class_name)])

    def add_pedestal(self) -> UIPieceBuilder:
        return self.add('pedestal')

    def add_pedestal_hole(self) -> UIPieceBuilder:
        return self.add('pedestal-hole')

    def add_foot(self) -> UIPieceBuilder:
        return self.add('foot')

    def add_foot_hole(self) -> UIPieceBuilder:
        return self.add('foot-hole')

    def add_body(self) -> UIPieceBuilder:
        return self.add('body')

    def add_body_hole(self) -> UIPieceBuilder:
        return self.add('body-hole')

    def add_body_fill(self) -> UIPieceBuilder:
        return self.add('body-fill')

    def add_shoulder(self) -> UIPieceBuilder:
        return self.add('shoulder')

    def add_shoulder_hole(self) -> UIPieceBuilder:
        return self.add('shoulder-hole')

    def add_shoulder_fill(self) -> UIPieceBuilder:
        return self.add('shoulder-fill')

    def add_head(self) -> UIPieceBuilder:
        return self.add('head')

    def add_head_hole(self) -> UIPieceBuilder:
        return self.add('head-hole')

    def add_head_fill(self) -> UIPieceBuilder:
        return self.add('head-fill')


class UIPiece(ABC, Div):
    def __init__(self, color: Color, **kwargs):
        self.color = color
        self.builder = UIPieceBuilder(self.piece, self.color)
        super().__init__(children=self.build_piece(), **kwargs)

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


class UIPawn(UIPiece):
    @property
    def piece(self) -> PieceOption:
        return PieceOption.PAWN

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
            .build()

    def build_white_piece(self) -> Div:
        return self.builder \
            .add_pedestal() \
            .add_pedestal_hole() \
            .add_foot() \
            .add_foot_hole() \
            .add_body() \
            .add_body_fill() \
            .add_shoulder() \
            .add_shoulder_hole() \
            .add_head() \
            .add_head_hole() \
            .build()


self = UIPawn(color=Color.WHITE)
