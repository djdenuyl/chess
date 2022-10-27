"""
Created on 2022-10-22
@author: David den Uyl (djdenuyl@gmail.com)
"""
from dash import Dash, Input, Output, ctx, State, ALL
from dash.exceptions import PreventUpdate
from dash.html import Div, Button
from src.game import Game
from typing import Optional
from utils.letters import LETTERS


class App:
    def __init__(self):
        self.dash = Dash()
        self.game: Game = Game()
        self.original_classes = []
        self.tiles = None
        self.selected_name = None

        self.dash.layout = self.layout
        self.callbacks()

    @property
    def layout(self):
        return Div(
            id='app-container',
            children=[
                Div(id='border', children=self.init_labels()),
                Div(
                    id='chessboard',
                    children=self.init_board()
                )
            ]
        )

    def play(self, **kwargs):
        """ play the game """
        self.dash.run(**kwargs)

    def init_board(self) -> list[Button]:
        """ initiate the game board. update the original classes of each tile"""
        buttons = []
        self.original_classes = []
        for row in self.game.board.tiles:
            for tile in row:
                class_name = f'tile {tile.color}'
                self.original_classes.append(class_name)
                buttons.append(
                    Button(
                        id={
                            'type': 'tile',
                            'index': tile.name
                        },
                        className=class_name,
                        children=str(tile.piece)
                    )
                )

        return buttons

    def init_labels(self) -> list[Div]:
        empty_div = Div('', className='label')

        labels = list()
        labels.append(empty_div)
        labels.extend([Div(i, className='letter') for i in LETTERS])
        labels.append(empty_div)
        for i, row in enumerate(self.game.board.tiles):
            labels.append(Div(i + 1, className='number'))
            for _ in row:
                labels.append(empty_div)
            labels.append(Div(i + 1, className='number'))
        # letters =
        # numbers = [Div(i, className='number') for i in range(1, 9)]

        # return letters + numbers
        return labels

    def reset_effects(self):
        """ reset the class for each tile to its original state"""
        # reset fx
        for i, _ in enumerate(self.tiles):
            self.tiles[i]['props']['className'] = self.original_classes[i]

    def update_effects(self, index: str, *, add: list[str]):
        """ update the class at tile 'index', add each element in 'add' not already in its class list"""
        for a in add:
            current_classes = self.tiles[self.game.board.index_by_name(index)]['props']['className']
            if a not in current_classes:
                self.tiles[self.game.board.index_by_name(index)]['props']['className'] = current_classes + ' ' + a

    def update_placement(self):
        """ update the children of all tiles with the current game state"""
        for i, _ in enumerate(self.tiles):
            self.tiles[i]['props']['children'] = str(self.game.board.tile_by_index(i).piece)

    def update_tiles(self) -> list[dict]:
        """ update the tiles, update the placements and effects"""
        self.update_placement()
        self.reset_effects()

        if self.selected_name is not None:
            self.update_effects(self.selected_name, add=['selected'])

        return self.tiles

    def update_selection(self, triggered_name):
        """ update the selection state depending on which index was triggered. """
        if self.selected_name is None \
                and self.game.board.tile_by_name(triggered_name).piece.color == self.game.turn:
            self.selected_name = triggered_name
        elif triggered_name == self.selected_name:
            self.selected_name = None
        elif triggered_name != self.selected_name and self.selected_name is not None:
            self.selected_name = triggered_name
        else:
            pass

    def log(self, is_player_checked: Optional[bool]):
        if self.selected_name is not None:
            print(f"its {self.game.turn.name}'s turn, "
                  f"{self.game.board.tile_by_name(self.selected_name).piece.__class__.__name__} at "
                  f"{self.selected_name} is selected")
        else:
            print(f"its {self.game.turn.name}'s turn, nothing is selected")

        if is_player_checked:
            print(f'player {self.game.turn.name} is in check')

    def callbacks(self):
        @self.dash.callback(
            Output('chessboard', 'children'),
            Input({'type': 'tile', 'index': ALL}, 'n_clicks'),
            State('chessboard', 'children'),
            prevent_initial_callback=True
        )
        def render(_, tiles):
            """ render a new frame of the game """
            if ctx.triggered_id is None:
                raise PreventUpdate

            triggered_name = ctx.triggered_id.get('index')

            # set the new tile state
            self.tiles = tiles

            is_player_checked = None
            if self.selected_name is not None:
                self.game.move(
                    self.game.board.tile_by_name(self.selected_name),
                    self.game.board.tile_by_name(triggered_name)
                )

                is_player_checked = self.game.check()
                # deselect after move attempt
                self.selected_name = None
            else:
                # update which piece is selected
                self.update_selection(triggered_name)

            self.log(is_player_checked)

            return self.update_tiles()


if __name__ == '__main__':
    app = App()
    app.play(debug=True)
