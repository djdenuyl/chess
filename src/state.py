"""
author: David den Uyl (djdenuyl@gmail.com)
date: 2022-10-19
"""
from enum import Enum


class State(Enum):
    CHECK = 'check'
    CHECKMATE = 'checkmate'
    STALEMATE = 'stalemate'
