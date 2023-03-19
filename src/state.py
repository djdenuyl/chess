"""
author: David den Uyl (djdenuyl@gmail.com)
date: 2022-10-19
"""
from enum import Enum


class State(Enum):
    """ The possible states a player can be in """
    CHECK = 'check'
    CHECKMATE = 'checkmate'
    STALEMATE = 'stalemate'
    OUT_OF_TIME = 'out_of_time'
