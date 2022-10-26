"""
Created on 2022-10-19
@author: David den Uyl (djdenuyl@gmail.com)
"""
from src.player import WHITE_PLAYER, BLACK_PLAYER
from src.tile import Tile
from src.board import Board
from utils.letters import LETTERS


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
                    self.board.tiles[self.board.height - t.y][t.x_int].piece = k.value.get(player.color)

    @staticmethod
    def is_valid_move(frm: Tile, to: Tile) -> bool:
        """ check if the piece on the 'frm' Tile is allowed to move to the 'to' Tile"""
        return frm.piece.is_valid_move(frm, to)

    def move(self, frm: Tile, to: Tile):
        """ move a piece """
        if self.is_valid_move(frm, to):
            from_piece = frm.piece
            to_piece = to.piece

            self.board.tiles[self.board.height - to.y][to.x_int].piece = from_piece
            self.board.tiles[self.board.height - frm.y][frm.x_int].piece = to_piece

    def print(self):
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
