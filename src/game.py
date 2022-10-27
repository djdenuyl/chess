"""
Created on 2022-10-19
@author: David den Uyl (djdenuyl@gmail.com)
"""
from src.piece import Blank, Knight, King
from src.player import WHITE_PLAYER, BLACK_PLAYER
from src.tile import Tile
from src.board import Board
from utils.color import Color
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

    @property
    def opponent(self) -> Color:
        return Color.BLACK if self.turn == Color.WHITE else Color.WHITE

    def _init_pieces(self):
        for player in self.players:
            for k, v in player.start_positions.items():
                for t in v:
                    self.board.tiles[self.board.height - t.y][t.x_int].piece = k(player.color)

    def _is_valid_move(self, frm: Tile, to: Tile, player_color: Color) -> bool:
        """ check if the piece on the 'frm' Tile is allowed to move to the 'to' Tile"""
        return frm.piece.is_valid_move(frm, to) and self._has_clear_path(frm, to) and frm.piece.color == player_color

    def _has_clear_path(self, frm: Tile, to: Tile) -> bool:
        """ check if there are any pieces between the 'frm' tile and 'to' tile. return False if there are any"""
        # only knights ignore the clear path rule, other pieces obey
        if not isinstance(frm.piece, Knight):
            x_idx = self._horizontal_indices_between(frm, to)
            y_idx = self._vertical_indices_between(frm, to)
            tiles = [self.board.tiles[self.board.height - y][x] for x, y in zip(x_idx, y_idx)]

            # if any of the tiles between frm and to is not a Blank tile, the path is not clear
            for t in tiles:
                if not isinstance(t.piece, Blank):
                    return False

        return True

    @staticmethod
    def _horizontal_indices_between(frm: Tile, to: Tile) -> range:
        """ collect the axis indices horizontally between the frm and to tile"""
        drc, lng = get_vector(frm, to)
        return range(frm.x_int + drc.value[0], to.x_int, drc.value[0] or 1) or [frm.x_int] * (abs(lng.dy) - 1)

    @staticmethod
    def _vertical_indices_between(frm: Tile, to: Tile) -> range:
        """ collect the axis indices vertically between the frm and to tile"""
        drc, lng = get_vector(frm, to)
        return range(frm.y + drc.value[1], to.y, drc.value[1] or 1) or [frm.y] * (abs(lng.dx) - 1)

    def move(self, frm: Tile, to: Tile):
        """ move a piece"""
        if self._is_valid_move(frm, to, self.turn):
            from_piece = frm.piece

            self.board.tiles[self.board.height - to.y][to.x_int].piece = from_piece
            self.board.tiles[self.board.height - frm.y][frm.x_int].piece = Blank()

            # set the turn to the other player
            self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE

    def check(self) -> bool:
        """ checks for the player who's turn it is whether its king is checked"""
        king_tile, *_ = [t for t in self.board.flat if isinstance(t.piece, King) and t.piece.color == self.turn]

        opponent_tiles = [
            t for t in self.board.flat if t.piece.color != self.turn and not isinstance(t.piece, Blank)
        ]

        if any([self._is_valid_move(tile, king_tile, self.opponent) for tile in opponent_tiles]):
            return True

        return False

    def print(self):
        """ print out the current board state"""
        print('  ' + '  '.join(LETTERS, ))
        for y in self.board.tiles:
            print(f"{y[0].y} {' '.join([str(x.piece) or x.color for x in y])} {y[0].y}")

        print('  ' + '  '.join(LETTERS, ))


def main():
    game = Game()
    game.print()

    playing = True
    while playing:
        action = input('Enter tile to move piece from and to: (comma separated): ')

        if action == 'q':
            playing = False
            continue

        try:
            frm, to = [a.strip().upper() for a in action.split(',')]
            print(frm, '->', to)
            game.move(
                game.board.tile_by_name(frm),
                game.board.tile_by_name(to)
            )
        except ValueError:
            print(f'could not parse action: {action}')
            continue

        game.print()


if __name__ == '__main__':
    main()
