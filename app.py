"""
Created on 2022-10-22
@author: David den Uyl (djdenuyl@gmail.com)
"""
from dash import Dash, Input, Output, ctx, State, ALL
from dash.exceptions import PreventUpdate
from dash.html import Div, Button
from lib.game import Game


class App:
    def __init__(self):
        self.dash = Dash()
        self.game = Game()
        self.dash.layout = self.layout
        self.callbacks()

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
                        id={
                            'type': 'tile',
                            'index': tile.name
                        },
                        className=f'tile {tile.color}',
                        children=tile.piece
                    )
                )

        return buttons

    def update_tiles(self, tiles: list):
        for i, _ in enumerate(tiles):
            # TODO: you are here
            tiles[i]['props']['children'] = self.game.board.get_tile(i).piece

        return tiles

    def callbacks(self):
        @self.dash.callback(
            Output('chessboard', 'children'),
            Input({'type': 'tile', 'index': ALL}, 'n_clicks'),
            State('chessboard', 'children'),
            prevent_initial_callback=True
        )
        def render(tiles):
            if ctx.triggered_id is None:
                raise PreventUpdate

            return self.update_tiles(tiles)


if __name__ == '__main__':
    app = App()
    app.play(debug=True)
