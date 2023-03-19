"""
Clock UI element

author: David den Uyl (djdenuyl@gmail.nl)
date: 2023-03-19
"""
from dash.html import Div


class Clock(Div):
    __time = '20:00'

    def __init__(self, time: str = __time, **kwargs):
        self.time = time

        super().__init__(children=self.time, **kwargs)
