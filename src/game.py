"""
Created on 2022-10-19
@author: David den Uyl (djdenuyl@gmail.com)
"""
from itertools import compress
from src.piece import Blank, King
from src.player import WHITE_PLAYER, BLACK_PLAYER
from src.state import State
from src.tile import Tile
from src.board import Board
from typing import Iterator, Optional
from utils.color import Color, opponent
from utils.letters import LETTERS


class Game:
    def __init__(self):
        self.board = Board()
        self.white = WHITE_PLAYER
        self.black = BLACK_PLAYER
        self.players = [self.white, self.black]
        self.turn = Color.WHITE
        self._init_pieces()

    def _init_pieces(self):
        for player in self.players:
            for k, v in player.start_positions.items():
                for t in v:
                    self.board.tiles[self.board.height - t.y][t.x_int].piece = k(player.color)

    def _is_valid_move(self, frm: Tile, to: Tile) -> bool:
        """ check if the piece on the 'frm' Tile is allowed to move to the 'to' Tile"""
        return frm.piece.is_valid_move(frm, to) and self._has_clear_path(frm, to)

    def _has_clear_path(self, frm: Tile, to: Tile) -> bool:
        """ check if there are any pieces between the 'frm' tile and 'to' tile. return False if there are any"""
        tiles = self.board.tiles_between(frm, to)

        # if any of the tiles between frm and to is not a Blank tile, the path is not clear
        for t in tiles:
            if not isinstance(t.piece, Blank):
                return False

        return True

    def _is_under_thread_by(self, tile) -> Iterator[Tile]:
        """ returns a list of all opponent occupied tiles that can reach the tile within one move"""
        if isinstance(tile.piece, Blank):
            return []

        opponent_tiles = self.board.opponent_tiles(tile)

        # if any of the opponents pieces can make a valid move to the piece
        return compress(opponent_tiles, [self._is_valid_move(opponent_tile, tile) for opponent_tile in opponent_tiles])

    def _is_under_thread(self, tile) -> bool:
        """ check if a tile is reachable by a piece from the opponent within one move"""
        if isinstance(tile.piece, Blank):
            return False

        # if any of the opponents pieces can make a valid move to the piece
        if any(self._is_under_thread_by(tile)):
            return True

        return False

    def _cant_move_king(self) -> bool:
        """ check if the player whose turn it is can move his king from its current tile"""
        king_tile, *_ = self.board.tiles_by_piece_type(King, self.turn)
        surrounding_tiles = self.board.surrounding_tiles(king_tile)

        return all([not self._is_valid_move(king_tile, s) or self._is_under_thread(s) for s in surrounding_tiles])

    def _can_move_piece_between_king(self) -> bool:
        """ checks if any piece can be moved between the king and any piece threatening the king
        TODO: does this also work for double checks?"""
        king_tile, *_ = self.board.tiles_by_piece_type(King, self.turn)
        threatening_tiles = self._is_under_thread_by(king_tile)
        own_tiles = self.board.tiles_by_color(self.turn)

        for threatening_tile in threatening_tiles:
            between_tiles = self.board.tiles_between(threatening_tile, king_tile)
            for between_tile in between_tiles:
                for own_tile in own_tiles:
                    return self._is_valid_move(own_tile, between_tile)

        return False

    def _can_take_piece_threatening_king(self) -> bool:
        """ checks if any piece can take the piece threatening the king"""
        king_tile, *_ = self.board.tiles_by_piece_type(King, self.turn)
        threatening_tiles = self._is_under_thread_by(king_tile)
        if any([self._is_under_thread(tt) for tt in threatening_tiles]):
            return True

        return False

    def move(self, frm: Tile, to: Tile):
        """ move a piece"""
        if self._is_valid_move(frm, to) and frm.piece.color == self.turn:
            frm_piece = frm.piece
            to_piece = to.piece

            self.board.tiles[self.board.height - to.y][to.x_int].piece = frm_piece
            self.board.tiles[self.board.height - frm.y][frm.x_int].piece = Blank()

            # if the move results in a check state, revert the move
            if self.check():
                self.board.tiles[self.board.height - to.y][to.x_int].piece = to_piece
                self.board.tiles[self.board.height - frm.y][frm.x_int].piece = frm_piece
                return

            # update that the piece (now at the to tile) has moved
            self.board.tiles[self.board.height - to.y][to.x_int].piece.has_moved = True
            # set the turn to the other player
            self.turn = opponent(self.turn)

    def check(self) -> bool:
        """ checks for the player who's turn it is whether its king is in check"""
        king_tile, *_ = self.board.tiles_by_piece_type(King, self.turn)

        return self._is_under_thread(king_tile)

    def checkmate(self) -> bool:
        """ checks for the player who's turn it is whether its checkmate"""
        # 1) the king is in check
        # 2) all tiles around the king are either an invalid move for the king or result in a check
        # 3) and no piece can be put in between the king and the piece that has the king in check
        # 4) no piece can take the piece that has the king in check
        if self.check() \
                and self._cant_move_king() \
                and not self._can_move_piece_between_king() \
                and not self._can_take_piece_threatening_king():
            return True

        return False

    def state(self) -> Optional[State]:
        """ return the current game state """
        if self.checkmate():
            return State.CHECKMATE
        elif self.check():
            return State.CHECK
        else:
            return

    def print(self):
        """ print out the current board state"""
        print('  ' + '  '.join(LETTERS, ))
        for y in self.board.tiles:
            print(f"{y[0].y} {' '.join([str(x.piece) or x.color for x in y])} {y[0].y}")

        print('  ' + '  '.join(LETTERS, ))
