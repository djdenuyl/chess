"""
Created on %(date)s

@author: David den Uyl (ddenuyl@bebr.nl)
"""
from src.piece import Knight, Pawn, Bishop, Queen, King, Rook
from ui.pieces.bishop import UIBishop
from ui.pieces.king import UIKing
from ui.pieces.pawn import UIPawn
from ui.pieces.knight import UIKnight
from ui.pieces.queen import UIQueen
from ui.pieces.rook import UIRook


# UI_PIECE_MAPPER = {
#     Bishop: UIBishop,
#     King: UIKing,
#     Knight: UIKnight,
#     Pawn: UIPawn,
#     Queen: UIQueen,
#     Rook: UIRook,
# }

UI_PIECE_MAPPER = {
    Bishop: UIPawn,
    King: UIPawn,
    Knight: UIPawn,
    Pawn: UIPawn,
    Queen: UIPawn,
    Rook: UIPawn,
}
