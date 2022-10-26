"""
Created on 2022-10-19
@author: David den Uyl (djdenuyl@gmail.com)
"""
from dataclasses import dataclass, field
from itertools import chain
from string import ascii_uppercase
from src.player import WHITE_PLAYER, BLACK_PLAYER, PieceOption

LETTERS = list(ascii_uppercase)[:8]


@dataclass
class Tile:
    x: str = field(repr=False)
    y: int = field(repr=False)
    x_int: int = field(init=False, repr=False)
    name: str = field(init=False)
    piece: str = ''
    color: str = field(init=False)

    def __set_x_int(self):
        self.x_int = LETTERS.index(self.x)

    def __set_name(self):
        self.name = f'{self.x}{self.y}'

    def __set_color(self):
        # if the sum of the x and the y index is even, the tile is a black tile
        if (self.x_int + self.y) % 2 == 0:
            self.color = '⬛'
        else:
            self.color = '⬜'

    def __post_init__(self):
        self.__set_x_int()
        self.__set_name()
        self.__set_color()


@dataclass
class Board:
    height: int = 8
    width: int = 8
    tiles: list[list[Tile]] = field(init=False)

    def __post_init__(self):
        self.__init_board()

    def __init_board(self):
        """ initialize an empty game board """
        self.tiles = [
            [
                Tile(LETTERS[w], self.height - h) for w in range(self.width)
            ] for h in range(self.height)
        ]

    def tile_by_index(self, idx) -> Tile:
        """ return a tile by its index """
        return list(chain(*self.tiles))[idx]

    def tile_by_name(self, name) -> Tile:
        """ return a tile by its name """
        tile, *_ = [t for t in list(chain(*self.tiles)) if t.name == name]
        return tile

    def index_by_name(self, name) -> int:
        """ return a tile index by its name"""
        return [i for i, tile in enumerate(chain(*self.tiles)) if tile.name == name][0]


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

    def is_valid_move(self, frm: Tile, to: Tile) -> bool:
        return True

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
            print(f"{y[0].y} {'  '.join([x.piece or x.color for x in y])} {y[0].y}")

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
            print(frm, to)
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
