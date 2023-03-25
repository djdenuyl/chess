"""
UI elements of the pawn piece

author: David den Uyl (djdenuyl@gmail.com)
date: 2023-03-23
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dash.html import Div
from re import findall
from src.piece import PieceOption, Pawn, Knight
from typing import Optional
from utils.color import Color
from utils.settings import PIECE_SCALE_FACTOR


class UIPieceBuilder:
    def __init__(self, parts: Optional[list] = None):
        self.parts = parts

        if self.parts is None:
            self.parts = []

    def build(self) -> Div:
        return Div(
            className='model',
            children=self.parts
        )

    def add(self, class_name: str, style: Optional[dict] = None) -> UIPieceBuilder:
        return type(self)(self.parts + [Div(className=class_name, style=style)])

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

    # def add_body_fill_hole(self) -> UIPieceBuilder:
    #     return self.add('body-fill-hole')

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

    def add_right_ear(self):
        return self.add('ear right')

    def add_left_ear(self):
        return self.add('ear left')

    def add_nose(self):
        return self.add('nose')

    def add_nose_hole(self):
        return self.add('nose-hole')

    def add_face(self):
        return self.add('face')

    def add_face_hole(self):
        return self.add('face-hole')

    def add_snout(self):
        return self.add('snout')

    def add_snout_outline(self):
        return self.add('snout-outline')

    def add_snout_hole(self):
        return self.add('snout-hole')

    def add_neck(self):
        return self.add('neck')

    def add_neck_hole(self):
        return self.add('neck-hole')

    def add_mane(self):
        s = PIECE_SCALE_FACTOR
        path = self.scale(
            'path("m 135.63534,127.03486 c 4.88867,-22.95693 17.6283,-34.301315 22.47599,-45.241118 21.37925,-48.246605 -8.60704,-77.5078523 -49.22096,-74.5211696 -2.36366,0.1738201 0.49151,11.1115656 0.49151,11.1115656 37.7491,-4.669007 53.61883,30.653212 35.9107,63.140057 -17.18396,10.367624 -11.49156,30.051845 -9.65724,45.510665 z")',
            s
        )

        return self.add(
            class_name='mane',
            style={'clipPath': path}
        )

    def add_mane_hole(self):
        s = PIECE_SCALE_FACTOR
        path = self.scale(
            ' path("m 135.63534,127.03486 c 4.88867,-22.95693 17.6283,-34.301315 22.47599,-45.241118 21.37925,-48.246605 -8.60704,-77.5078523 -49.22096,-74.5211696 -2.36366,0.1738201 0.49151,11.1115656 0.49151,11.1115656 37.7491,-4.669007 53.61883,30.653212 35.9107,63.140057 -17.18396,10.367624 -11.49156,30.051845 -9.65724,45.510665 z")',
            s
        )

        return self.add(
            class_name='mane-hole',
            style={'clipPath': path}
        )

    def add_nostril(self):
        return self.add('nostril')

    def add_eye(self):
        s = PIECE_SCALE_FACTOR
        path = self.scale('path("m 94.152597,36.113755 c 1.79209,8.351338 -5.312927,11.993216 -10.455928,9.205762 0.511566,-3.785635 7.137462,-9.392004 10.455928,-9.205762 z")', s)

        return self.add(
            class_name='eye',
            style={'clipPath': path}
        )

    def add_eye_outline(self):
        s = PIECE_SCALE_FACTOR
        path = self.scale('path("m 94.152597,36.113755 c 1.79209,8.351338 -5.312927,11.993216 -10.455928,9.205762 0.511566,-3.785635 7.137462,-9.392004 10.455928,-9.205762 z")', s)

        return self.add(
            class_name='eye-outline',
            style={'clipPath': path}
        )

    def add_upper_body(self):
        s = PIECE_SCALE_FACTOR
        path = self.scale('path("m 71.163998,135.97274 69.082802,0.28245 c -7.26058,-27.87536 -1.3983,-43.203455 7.54611,-53.594481 l -16.03137,-8.967442 c -4.10728,4.473023 -9.41986,5.309291 -15.55178,5.743013 0,0 -40.803041,26.93014 -45.045762,56.53646 z")', s)

        return self.add(
            class_name='upper-body',
            style={'clipPath': path}
        )

    def add_upper_body_fill(self):
        s = PIECE_SCALE_FACTOR
        path = self.scale('path("m 125.06577,137.14983 -10.00132,-0.4546 c -1.59597,-37.690256 5.037,-29.41556 20.31659,-51.73064 -16.41292,24.40487 -12.20498,36.3396 -10.31527,52.18524 z")', s)

        return self.add(
            class_name='upper-body-fill',
            style={'clipPath': path}
        )

    def add_upper_body_hole(self):
        s = PIECE_SCALE_FACTOR
        path = self.scale('path("m 133.14627,136.61487 -56.547486,-0.19895 c 5.190086,-13.96122 13.34471,-30.36957 41.306926,-48.941468 5.71546,0.757575 9.26207,1.031811 17.47533,-2.509862 -5.39554,16.68229 -7.94588,26.38518 -2.23477,51.65028 z")', s)
        return self.add(
            class_name='upper-body-hole',
            style={'clipPath': path}
        )

    @staticmethod
    def scale(path: str, s: float) -> str:
        """ apply scaling to svg path by scaling factor s"""
        # Extract all floats from the string using a regex
        floats = findall(r'[-+]?\d*\.\d+', path)

        # Scale each float by the scale factor and convert it to a string
        scaled_floats = [str(float(f) * s) for f in floats]

        # Replace the original floats with the scaled floats in the string
        for i in range(len(floats)):
            path = path.replace(floats[i], scaled_floats[i])

        return path


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
            .add_body_hole() \
            .add_body_fill() \
            .add_shoulder() \
            .add_shoulder_hole() \
            .add_head() \
            .add_head_hole() \
            .build()


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


UI_PIECE_MAPPER = {
    Knight: UIKnight,
    Pawn: UIPawn
}
