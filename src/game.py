"""
Created on 2022-10-19
@author: David den Uyl (djdenuyl@gmail.com)
"""
from src.piece import Blank, Knight
from src.player import WHITE_PLAYER, BLACK_PLAYER
from src.tile import Tile
from src.board import Board
from utils.direction import Direction, DIAGONAL_DIRECTIONS
from utils.letters import LETTERS
from utils.vector import get_vector


class Game:
    def __init__(self):
        self.board = Board()
        self.white = WHITE_PLAYER
        self.black = BLACK_PLAYER
        self.players = [self.white, self.black]
        self.__init_pieces()

    def __init_pieces(self):
        for player in self.players:
            for k, v in player.start_positions.items():
                for t in v:
                    self.board.tiles[self.board.height - t.y][t.x_int].piece = k(player.color)

    def is_valid_move(self, frm: Tile, to: Tile) -> bool:
        """ check if the piece on the 'frm' Tile is allowed to move to the 'to' Tile"""
        return frm.piece.is_valid_move(frm, to) and self.has_clear_path(frm, to)

    def has_clear_path(self, frm: Tile, to: Tile) -> bool:
        """ check if there are any pieces between the 'frm' tile and 'to' tile. return False if there are any"""
        # only knights ignore the clear path rule, other pieces obey
        if not isinstance(frm.piece, Knight):
            direction, length = get_vector(frm, to)
            if direction in (Direction.E, Direction.W):
                tiles = [
                    self.board.tiles[self.board.height - frm.y][x]
                    for x in range(frm.x_int + direction.value[0], to.x_int, direction.value[0])
                ]
            elif direction in (Direction.N, Direction.S):
                tiles = [
                    self.board.tiles[self.board.height - y][frm.x_int]
                    for y in range(frm.y + direction.value[1], to.y, direction.value[1])
                ]
            elif direction in DIAGONAL_DIRECTIONS:
                tiles = [
                    self.board.tiles[self.board.height - y][x]
                    for x, y in zip(
                        range(frm.x_int + direction.value[0], to.x_int, direction.value[0]),
                        range(frm.y + direction.value[1], to.y, direction.value[1])
                    )
                ]
            else:
                tiles = []

            # if any of the tiles between frm and to is not a Blank tile, the path is not clear
            for t in tiles:
                if not isinstance(t.piece, Blank):
                    return False

        return True

    def move(self, frm: Tile, to: Tile):
        """ move a piece """
        if self.is_valid_move(frm, to):
            from_piece = frm.piece

            self.board.tiles[self.board.height - to.y][to.x_int].piece = from_piece
            self.board.tiles[self.board.height - frm.y][frm.x_int].piece = Blank()

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
