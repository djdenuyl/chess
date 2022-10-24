"""
Created on 2022-10-22
@author: David den Uyl (djdenuyl@gmail.com)
"""
from dash import Dash
from dash.html import Div, Button
from lib.game import Game


class App:
    def __init__(self):
        self.dash = Dash()
        self.game = Game()
        self.dash.layout = self.layout

    @property
    def layout(self):
        return Div(
            id='app-container',
            children=[
                Div(id='border'),
                Div(
                    id='chessboard',
                    children=self.init_board()
                )
            ]
        )

    def play(self, **kwargs):
        self.dash.run(**kwargs)

    def init_board(self) -> list[Button]:
        buttons = []
        for row in self.game.board:
            for tile in row:
                buttons.append(
                    Button(
                        id=tile.name,
                        className=f'tile {tile.color}',
                        children=tile.piece
                    )
                )

        return buttons


if __name__ == '__main__':
    app = App()
    app.play(debug=True)
