from enum import Enum
from src.piece import Pawn, Rook, Knight, Bishop, Queen, King, Blank
from utils.color import Color


class PieceOption(Enum):
    PAWN = {Color.BLACK: Pawn(Color.BLACK), Color.WHITE: Pawn(Color.WHITE)}
    ROOK = {Color.BLACK: Rook(Color.BLACK), Color.WHITE: Rook(Color.WHITE)}
    KNIGHT = {Color.BLACK: Knight(Color.BLACK), Color.WHITE: Knight(Color.WHITE)}
    BISHOP = {Color.BLACK: Bishop(Color.BLACK), Color.WHITE: Bishop(Color.WHITE)}
    QUEEN = {Color.BLACK: Queen(Color.BLACK), Color.WHITE: Queen(Color.WHITE)}
    KING = {Color.BLACK: King(Color.BLACK), Color.WHITE: King(Color.WHITE)}
    BLANK = {Color.BLACK: Blank(), Color.WHITE: Blank()}
