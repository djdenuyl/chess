"""
Created on 2022-10-22
@author: David den Uyl (djdenuyl@gmail.com)
"""
from dash import Dash, Input, Output, ctx, State, ALL
from dash.exceptions import PreventUpdate
from dash.html import Div, Button
from src.game import Game
from typing import Optional


class App:
    def __init__(self):
        self.dash = Dash()
        self.game = Game()
        self.dash.layout = self.layout
        self.tiles = None
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
        for row in self.game.board.tiles:
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

    def update_classes(self, index: str, *, add: list[str]):
        for a in add:
            current_classes = self.tiles[self.game.board.name_to_index(index)]['props']['className']
            self.tiles[self.game.board.name_to_index(index)]['props']['className'] = current_classes + ' ' + a

    def update_tiles(self, triggered_id: Optional[str] = None) -> list[dict]:
        for i, _ in enumerate(self.tiles):
            self.tiles[i]['props']['children'] = self.game.board.tile_by_index(i).piece

        if triggered_id is not None:
            self.update_classes(triggered_id, add=['selected'])

        return self.tiles

    def callbacks(self):
        @self.dash.callback(
            Output('chessboard', 'children'),
            Input({'type': 'tile', 'index': ALL}, 'n_clicks'),
            State('chessboard', 'children'),
            prevent_initial_callback=True
        )
        def render(_, tiles):
            if ctx.triggered_id is None:
                raise PreventUpdate

            triggered_id = ctx.triggered_id.get('index')

            # set the new tile state
            self.tiles = tiles

            return self.update_tiles(triggered_id)


if __name__ == '__main__':
    app = App()
    app.play(debug=True)
