"""
The Dash application / UI for the game

author: David den Uyl (djdenuyl@gmail.com)
date: 2022-10-22
"""
from dash import Dash, Input, Output, ctx, State, ALL
from dash.exceptions import PreventUpdate
from dash.html import Div, Button
from src.game import Game
from src.piece import Queen, Rook, Knight, Bishop, PIECE_TYPE_MAPPER
from src.state import State as GameState
from typing import Optional
from utils.color import Color, opponent
from utils.letters import LETTERS


class App:
    def __init__(self):
        self.dash = Dash()
        self.game: Game = Game()
        self.original_classes = []
        self.tiles = None
        self.selected_tile_name = None

        self.dash.layout = self.layout
        self.callbacks()

    @property
    def layout(self):
        return Div(
            id='app-container',
            children=[
                Div(id='indicator', children=Div(id='signal', className='signal')),
                Div(id='promotion'),
                Div(
                    id='border',
                    children=self.init_labels()
                ),
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

    def init_promotion_tile(self, tile) -> Div:
        """ create a promotion tile, where a player can select which piece to promote a pawn to"""
        return Div(
            className='promotion-tile',
            style={
                'grid-row': f'{self.game.board.height - tile.y + 1} / span 1',
                'grid-column': f'{tile.x_int + 1} / span 1',
                'background': 'var(--white-tile)' if tile.color == '⬜' else 'var(--black-tile)'
            },
            children=[
                # opponent here looks weird, but promotion is checked after the move has completed, which technically
                # makes it the opponents turn
                Button(id={'type': 'promotion', 'index': 'queen'}, children=str(Queen(opponent(self.game.turn)))),
                Button(id={'type': 'promotion', 'index': 'bishop'}, children=str(Bishop(opponent(self.game.turn)))),
                Button(id={'type': 'promotion', 'index': 'knight'}, children=str(Knight(opponent(self.game.turn)))),
                Button(id={'type': 'promotion', 'index': 'rook'}, children=str(Rook(opponent(self.game.turn)))),
            ]
        )

    @staticmethod
    def init_labels() -> list[Div]:
        """ create the labels at the border of the chessboard"""
        top_letters = Div(className='label top letters', children=[Div(i) for i in LETTERS])
        lft_numbers = Div(className='label lft numbers', children=[Div(i) for i in range(8, 0, -1)])
        rgt_numbers = Div(className='label rgt numbers ', children=[Div(i) for i in range(8, 0, -1)])
        btm_letters = Div(className='label btm letters ', children=[Div(i) for i in LETTERS])
        return [top_letters, lft_numbers, rgt_numbers, btm_letters]

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

        if self.selected_tile_name is not None:
            self.update_effects(self.selected_tile_name, add=['selected'])

        return self.tiles

    def update_selection(self, triggered_tile_name):
        """ update the selection state depending on which index was triggered. """
        if self.selected_tile_name is None \
                and self.game.board.tile_by_name(triggered_tile_name).piece.color == self.game.turn:
            self.selected_tile_name = triggered_tile_name
        elif triggered_tile_name == self.selected_tile_name:
            self.selected_tile_name = None
        elif triggered_tile_name != self.selected_tile_name and self.selected_tile_name is not None:
            self.selected_tile_name = triggered_tile_name
        else:
            pass

    def log(self, state: Optional[GameState]):
        if self.selected_tile_name is not None:
            print(f"its {self.game.turn.name}'s turn, "
                  f"{self.game.board.tile_by_name(self.selected_tile_name).piece.__class__.__name__} at "
                  f"{self.selected_tile_name} is selected")
        else:
            print(f"its {self.game.turn.name}'s turn, nothing is selected")

        if state is not None:
            print(f'player {self.game.turn.name}: {state.name}')

    def callbacks(self):
        @self.dash.callback(
            Output('chessboard', 'children'),
            Output('promotion', 'children'),
            Input({'type': 'tile', 'index': ALL}, 'n_clicks'),
            Input({'type': 'promotion', 'index': ALL}, 'n_clicks'),
            State('chessboard', 'children'),
            prevent_initial_callback=True
        )
        def render(*args):
            """ render a new frame of the game """
            # check if a promotion event is ongoing
            promotion_tile = self.game.which_pawn_promotable()

            if ctx.triggered_id is None or self.game.state() == GameState.CHECKMATE:
                raise PreventUpdate
            # if clicked on a tile
            elif ctx.triggered_id.get('type') == 'tile':
                # defer clicks on tiles when a promotion event is ongoing
                if promotion_tile is not None:
                    print('promotion event ongoing')
                    raise PreventUpdate
                # regular turn
                else:
                    triggered_tile_name = ctx.triggered_id.get('index')

                    # set the new tile state
                    self.tiles = args[-1]

                    game_state = None
                    if self.selected_tile_name is not None:
                        self.game.move(
                            self.game.board.tile_by_name(self.selected_tile_name),
                            self.game.board.tile_by_name(triggered_tile_name)
                        )

                        game_state = self.game.state()
                        # deselect after move attempt
                        self.selected_tile_name = None
                    else:
                        # update which piece is selected
                        self.update_selection(triggered_tile_name)

                    self.log(game_state)

                    updated_tiles = self.update_tiles()

                    # check if a promotion event is triggered
                    promotion_tile = self.game.which_pawn_promotable()
                    if promotion_tile is not None:
                        print('promotion event started')
                        return updated_tiles, self.init_promotion_tile(promotion_tile)

                    # if not, finish regular turn
                    return updated_tiles, None

            # if clicked on a promotion tile
            elif ctx.triggered_id.get('type') == 'promotion':
                # promote the pawn to the selected type
                self.game.promote(
                    promotion_tile,
                    piece_type=PIECE_TYPE_MAPPER.get(
                        ctx.triggered_id.get('index')
                    )
                )
                print('promotion event finished')

                return self.update_tiles(), None
            else:
                raise ValueError()

        @self.dash.callback(
            Output('signal', 'className'),
            Input('chessboard', 'children')
        )
        def update_indicator(_):
            clss = ['signal']
            if self.game.turn == Color.BLACK:
                clss.append('move')
            if self.game.check():
                clss.append('check')
            if self.game.checkmate():
                clss.append('checkmate')

            return ' '.join(clss)


if __name__ == '__main__':
    app = App()
    app.play(debug=True)
