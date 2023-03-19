"""
New Icon UI component

author: David den Uyl (djdenuyl@gmail.nl)
date: 2023-03-19
"""
from dash.html import Div


def new_icon() -> Div:
    return Div(
        className='new-icon',
        children=[
            Div(
                className='outer',
                children=[
                    Div(className='inner'),
                    Div(className='gap'),
                    Div(className='arrowhead')
                ]
            ),
        ]
    )


def help_icon() -> Div:
    return Div(
        className='help-icon',
        children=[
            Div(
                className='letter',
                children=[
                    Div(className='dot'),
                    Div(className='stem'),
                ]
            ),
        ]
    )


def timer_icon() -> Div:
    return Div(
        className='timer-icon',
        children=[
            Div(
                className='v',
                children=[
                    Div(className='sand-top'),
                    Div(className='sand-bottom'),
                ]
            ),
        ]
    )

