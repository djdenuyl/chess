"""
Created on 2022-10-19
@author: David den Uyl (djdenuyl@gmail.com)
"""
from dataclasses import dataclass, field
from itertools import chain
from typing import Optional
from lib.player import WHITE_PLAYER, BLACK_PLAYER, PieceOption

LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


@dataclass
class Tile:
    x: str = field(repr=False)
    y: int = field(repr=False)
    name: str = field(init=False)
    piece: Optional[PieceOption] = None
    color: str = field(init=False)

    def __post_init__(self):
        # if the sum of the x and the y index is even, the tile is a black tile
        if (LETTERS.index(self.x) + self.y) % 2 == 0:
            self.color = '⬛'
        else:
            self.color = '⬜'

        self.name = f'{self.x}{self.y}'


@dataclass
class Board:
    height: int = 8
    width: int = 8
    tiles: list[list[Tile]] = field(init=False)

    def __post_init__(self):
        self.tiles = self.__init_board()

    def __init_board(self):
        return [
            [
                Tile(LETTERS[w], 8 - h) for w in range(self.width)
            ] for h in range(self.height)
        ]

    def get_tile(self, idx):
        return list(chain(*self.tiles))[idx]


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
                for x, y in v:
                    self.board.tiles[int(y) - 1][LETTERS.index(x)].piece = k.value.get(player.color)

    def print(self):
        print('  ' + '  '.join(LETTERS, ))
        for y in self.board.tiles:
            print(f"{y[0].y} {'  '.join([x.color for x in y])} {y[0].y}")

        print('  ' + '  '.join(LETTERS, ))


def main():
    game = Game()
    game.print()

    playing = True
    while playing:
        action = input('Enter tile to move piece from and to: (comma separated): ')

        try:
            frm, to = action.split(',')
            print(frm, to)
        except ValueError:
            print(f'could not parse action: {action}')
            continue


if __name__ == '__main__':
    main()
