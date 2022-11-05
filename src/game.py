"""
Created on 2022-10-19
@author: David den Uyl (djdenuyl@gmail.com)
"""
from itertools import compress
from src.piece import Blank, King, PieceType, Pawn, Queen, Bishop, Knight, Rook
from src.player import WHITE_PLAYER, BLACK_PLAYER
from src.state import State
from src.tile import Tile
from src.board import Board
from typing import Iterator, Optional, Type
from utils.color import Color, opponent
from utils.letters import LETTERS
from utils.vector import get_vector


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

    def _is_under_thread_by(self, tile: Tile) -> Iterator[Tile]:
        """ returns a list of all opponent occupied tiles that can reach the tile within one move"""
        opponent_tiles = self.board.opponent_tiles(self.turn)

        # if any of the opponents pieces can make a valid move to the piece
        return compress(opponent_tiles, [self._is_valid_move(opponent_tile, tile) for opponent_tile in opponent_tiles])

    def _is_under_threat(self, tile: Tile) -> bool:
        """ check if a tile is reachable by a piece from the opponent within one move"""
        # if any of the opponents pieces can make a valid move to the piece
        if any(self._is_under_thread_by(tile)):
            return True

        return False

    def _cant_move_king(self) -> bool:
        """ check if the player whose turn it is can move his king from its current tile"""
        [king_tile] = self.board.tiles_by_piece_type(King, self.turn)
        surrounding_tiles = self.board.surrounding_tiles(king_tile)

        # TODO: There is still a bug here, where the game thinks the king is not under threat on a tile
        # TODO: currently blocked by the king itself, because the piece threatening the king doesnt have a clear
        # TODO: path. for example   this tile is currently not under threat -> [ ] [K] [<-] [<-] [R]
        print([s.name for s in surrounding_tiles])
        print([self._is_valid_move(king_tile, s) for s in surrounding_tiles])
        print([not self._is_under_threat(Tile(s.x, s.y)) for s in surrounding_tiles])
        print([self._is_valid_move(king_tile, s) and not self._is_under_threat(Tile(s.x, s.y)) for s in surrounding_tiles])
        # king can be moved if there is any move that is valid and not under threat, return negation of that
        # NB. We are considering the tile to be under threat if a piece can be moved there if it was not occupied
        # by a piece of its own color
        return not any(
            [self._is_valid_move(king_tile, s) and not self._is_under_threat(Tile(s.x, s.y)) for s in surrounding_tiles]
        )

    def _can_move_piece_between_king(self) -> bool:
        """ checks if any piece can be moved between the king and any piece threatening the king
        TODO: does this also work for double checks?"""
        [king_tile] = self.board.tiles_by_piece_type(King, self.turn)
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
        [king_tile] = self.board.tiles_by_piece_type(King, self.turn)
        threatening_tiles = self._is_under_thread_by(king_tile)
        if any([self._is_under_threat(tt) for tt in threatening_tiles]):
            return True

        return False

    def _en_passant(self, frm: Tile, to: Tile) -> Optional[Tile]:
        """ checks whether the move is eligible for en passant. Return the pawn that is passed if it is en passant"""
        direction, length = get_vector(frm, to)

        neighbor_tile = self.board.tiles[self.board.height - frm.y][frm.x_int + direction.value[0]]

        if isinstance(frm.piece, Pawn) \
                and frm.piece.is_valid_diagonal_move(direction, length) \
                and isinstance(neighbor_tile.piece, Pawn) \
                and neighbor_tile.piece.color != frm.piece.color \
                and neighbor_tile.piece.is_passable:
            return neighbor_tile

    def _castle(self, frm: Tile, to: Tile) -> bool:
        """ checks whether the move is eligible for castling."""
        if (isinstance(frm.piece, King) or isinstance(to.piece, King)) \
                and (isinstance(frm.piece, Rook) or isinstance(to.piece, Rook)) \
                and frm.piece.color == to.piece.color \
                and not frm.piece.has_moved \
                and not to.piece.has_moved \
                and self._has_clear_path(frm, to) \
                and not any(self._is_under_threat(tile) for tile in self.board.tiles_between(frm, to)) \
                and not self.check():
            return True

        return False

    def _resolve_castle(self, frm: Tile, to: Tile):
        """ take all actions needed to accomplish a castling move, i.e. moving and updating the King and Rook"""
        [k_tile] = self.board.tiles_by_piece_type(King, self.turn)
        [r_tile] = [r for r in self.board.tiles_by_piece_type(Rook, self.turn) if r in (frm, to)]
        kx = k_tile.x_int + 2 if r_tile.x == 'H' else k_tile.x_int - 2
        rx = kx - 1 if r_tile.x == 'H' else kx + 1
        self.board.tiles[self.board.height - k_tile.y][kx].piece = k_tile.piece
        self.board.tiles[self.board.height - k_tile.y][kx].piece.has_moved = True
        self.board.tiles[self.board.height - r_tile.y][rx].piece = r_tile.piece
        self.board.tiles[self.board.height - r_tile.y][rx].piece.has_moved = True
        self.board.tiles[self.board.height - to.y][to.x_int].piece = Blank()

    def move(self, frm: Tile, to: Tile):
        """ move a piece"""
        # reset pawns of the player whose turn it is to not passable
        self.board.reset_passable_pawns(self.turn)

        # check if en passant rule applies
        passable_pawn_tile = self._en_passant(frm, to)

        # check move conditions
        if (self._is_valid_move(frm, to) or passable_pawn_tile is not None or self._castle(frm, to)) \
                and frm.piece.color == self.turn:
            frm_piece = frm.piece
            to_piece = to.piece

            # update the tiles
            if self._castle(frm, to):
                self._resolve_castle(frm, to)
            else:
                # update the 'to' tile in case of a regular turn and that the piece (now at the 'to' tile) has moved
                self.board.tiles[self.board.height - to.y][to.x_int].piece = frm_piece
                self.board.tiles[self.board.height - to.y][to.x_int].piece.has_moved = True

            # the frm tile is always left empty
            self.board.tiles[self.board.height - frm.y][frm.x_int].piece = Blank()

            # if the move results in a check state, revert the move
            if self.check():
                self.board.tiles[self.board.height - to.y][to.x_int].piece = to_piece
                self.board.tiles[self.board.height - frm.y][frm.x_int].piece = frm_piece
                return

            # if the move is a valid en-passant move, remove the pawn that was passed
            if passable_pawn_tile is not None:
                self.board.tiles[self.board.height - passable_pawn_tile.y][passable_pawn_tile.x_int].piece = Blank()

            # set the turn to the other player
            self.turn = opponent(self.turn)

    def check(self) -> bool:
        """ checks for the player who's turn it is whether its king is in check"""
        [king_tile] = self.board.tiles_by_piece_type(King, self.turn)

        return self._is_under_threat(king_tile)

    def checkmate(self) -> bool:
        """ checks for the player who's turn it is whether its checkmate"""
        # 1) the king is in check
        # 2) all tiles around the king are either an invalid move for the king or result in a check
        # 3) and no piece can be put in between the king and the piece that has the king in check
        # 4) no piece can take the piece that has the king in check
        print(self.check())
        print(self._cant_move_king())
        print(not self._can_move_piece_between_king())
        print(not self._can_take_piece_threatening_king())

        if self.check() \
                and self._cant_move_king() \
                and not self._can_move_piece_between_king() \
                and not self._can_take_piece_threatening_king():
            return True

        return False

    def promote(self, pawn_tile: Tile, piece_type: Type[PieceType]):
        """ promotes a pawn to another piece when it reaches the other side """
        if not isinstance(pawn_tile.piece, Pawn) \
                or not any(piece_type == p for p in (Queen, Bishop, Knight, Rook)):
            return

        self.board.tiles[self.board.height - pawn_tile.y][pawn_tile.x_int].piece = \
            piece_type(color=pawn_tile.piece.color)

    def which_pawn_promotable(self) -> Optional[Tile]:
        """ checks if any pawn of the player whose turn it is, is in a position to be promoted and returns the
        tile containing the pawn that is promotable"""
        for tile in self.board.tiles_by_piece_type(Pawn):
            if tile.y in (1, 8):
                return tile

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
