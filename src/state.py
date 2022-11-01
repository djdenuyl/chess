"""
Created on %(date)s

@author: David den Uyl (ddenuyl@bebr.nl)
"""
from enum import Enum


class State(Enum):
    CHECK = 'check'
    CHECKMATE = 'checkmate'
    STALEMATE = 'stalemate'
