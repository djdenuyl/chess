"""
Icon UI components

author: David den Uyl (djdenuyl@gmail.nl)
date: 2023-03-19
"""
from dash.html import Div


class NewIcon(Div):
    def __init__(self, **kwargs):
        self.className = 'new-icon'
        super().__init__(className=self.className, children=self.icon, **kwargs)

    @property
    def icon(self) -> list[Div]:
        return [
            Div(
                className='outer',
                children=[
                    Div(className='inner'),
                    Div(className='gap'),
                    Div(className='arrowhead')
                ]
            ),
        ]


class HelpIcon(Div):
    def __init__(self, **kwargs):
        self.className = 'help-icon'
        super().__init__(className=self.className, children=self.icon, **kwargs)

    @property
    def icon(self) -> list[Div]:
        return [
            Div(
                className='letter',
                children=[
                    Div(className='dot'),
                    Div(className='stem'),
                ]
            ),
        ]


class TimerIcon(Div):
    def __init__(self, **kwargs):
        self.className = 'timer-icon'
        super().__init__(className=self.className, children=self.icon, **kwargs)

    @property
    def icon(self) -> list[Div]:
        return [
            Div(
                className='v',
                children=[
                    Div(className='sand-top'),
                    Div(className='sand-bottom'),
                ]
            ),
        ]
