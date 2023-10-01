"""
The Dash application / UI for the game

TODO: bug - game does not correctly check if any piece can take the piece that is checking the king.

author: David den Uyl (djdenuyl@gmail.com)
date: 2022-10-22
"""
from dash import Dash, Input, Output, ctx, State, ALL
from dash.dcc import Interval, Store
from dash.exceptions import PreventUpdate
from dash.html import Div, Button
from dash_unload_component import Unload
from dash_svg import Svg
from flask import Flask
from itertools import product
from parsers.svg import SVGParser
from pathlib import Path
from random import randint
from src.game import Game
from src.piece import Queen, Rook, Knight, Bishop, PIECE_TYPE_MAPPER, PieceOption, PieceType
from src.state import State as GameState
from src.tile import Tile
from typing import Optional
from ui.clock import Clock
from ui.icons import NewIcon, HelpIcon, TimerIcon
from utils.color import Color, opponent
from utils.letters import LETTERS
from utils.time import time_int_to_str


class App(Dash):
    def __init__(self, *args, **kwargs):
        super() \
            .__init__(
            server=Flask(__name__),
            *args,
            **kwargs
        )

        self.games: dict[str: Game] = {}
        self.original_classes = []
        self.assets = self.load_assets()

        # last step in the constructor is to set up the dash app
        self.setup()

    def setup(self):
        """ set up the dash app by adding the layout and the callbacks """
        self.layout = self.content
        self.callbacks()

    @property
    def content(self) -> Div:
        return Div(
            id='app-container',
            children=[
                Store(id='game_id_store'),  # stores the id of the game
                Store(id='new_game_event_store'),  # stores the event of starting a new game, use to update signal
                Store(id='selected_tile_store'),  # stores the currently selected tile
                Store(id='help_store'),  # stores whether the help function is activated
                Store(id='timer_store'),  # stores whether the timer is activated
                Store(id='tile_store'),  # stores the current state of the tiles
                Div(id='menu', children=self.init_menu_items()),
                Div(id='indicator', children=Div(id='signal', className='signal')),
                Div(id='clocks', className='clocks', children=[
                    Interval(id='ticker', disabled=True), Div(id='black-clock'), Div(id='white-clock')
                ]),
                Div(id='promotion'),
                Div(id='border', children=self.init_labels()),
                Div(id='chessboard'),
                Unload(id='unloader'),
            ]
        )

    def game(self, game_id: str) -> Game:
        return self.games.get(game_id)

    @staticmethod
    def init_menu_items() -> list[Button]:
        """ create the menu items """
        return [
            Button(id='new', className='new menu-item', children=NewIcon()),
            Button(id='help', className='help menu-item', children=HelpIcon()),
            Button(id='timer', className='timer menu-item', children=TimerIcon())
        ]

    def init_clocks(self, game_id: str) -> Optional[list[Div]]:
        """ create the time clocks """
        return [
            Interval(id='ticker', interval=1_000, disabled=True),
            Clock(id='black-clock', className='clock', time=time_int_to_str(self.games.get(game_id).time)),
            Clock(id='white-clock', className='clock', time=time_int_to_str(self.game(game_id).time)),
        ]

    def init_board(self, game_id: str) -> list[Button]:
        """ initiate the game board. update the original classes of each tile"""
        buttons = []
        self.original_classes = []
        for row in self.game(game_id).board.tiles:
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
                        children=self.get_piece_asset(tile.piece)
                    )
                )

        return buttons

    def init_promotion_tile(self, game_id: str, tile: Tile) -> Div:
        """ create a promotion tile, where a player can select which piece to promote a pawn to"""
        return Div(
            className='promotion-tile',
            style={
                'grid-row': f'{self.game(game_id).board.height - tile.y + 1} / span 1',
                'grid-column': f'{tile.x_int + 1} / span 1',
                'background': 'var(--white-tile)' if tile.color == '⬜' else 'var(--black-tile)'
            },
            children=[
                # opponent here looks weird, but promotion is checked after the move has completed, which technically
                # makes it the opponents turn
                Button(
                    id={'type': 'promotion', 'index': 'queen'},
                    children=self.get_piece_asset(Queen(opponent(self.game(game_id).turn)))
                ),
                Button(
                    id={'type': 'promotion', 'index': 'bishop'},
                    children=self.get_piece_asset(Bishop(opponent(self.game(game_id).turn)))
                ),
                Button(
                    id={'type': 'promotion', 'index': 'knight'},
                    children=self.get_piece_asset(Knight(opponent(self.game(game_id).turn)))
                ),
                Button(
                    id={'type': 'promotion', 'index': 'rook'},
                    children=self.get_piece_asset(Rook(opponent(self.game(game_id).turn)))
                ),
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

    @staticmethod
    def load_assets() -> dict[str: Svg]:
        """ load all the piece assets """
        svgs = {}
        for piece_type, color in product(PieceOption, Color.members()):
            symbol = str(PIECE_TYPE_MAPPER.get(piece_type.value)(color))

            svgs |= {
                symbol: SVGParser
                .from_file(
                    file=Path('assets', 'pieces', color.value, f'{piece_type.value}.svg'),
                    fill='#264653',
                    stroke_width=0
                )
                .parse_svg(
                    with_color=False,
                    classes=['piece']
                )
            }

        return svgs

    def reset_effects(self, tiles: list[dict]) -> list[dict]:
        """ reset the class for each tile to its original state"""
        # reset fx
        for i, _ in enumerate(tiles):
            tiles[i]['props']['className'] = self.original_classes[i]

        return tiles

    def update_effects(self, game_id: str, tiles: list[dict], index: str, *, add: list[str]) -> list[dict]:
        """ update the class at tile 'index', add each element in 'add' not already in its class list"""
        for a in add:
            current_classes = tiles[self.game(game_id).board.index_by_name(index)]['props']['className']
            if a not in current_classes:
                tiles[self.game(game_id).board.index_by_name(index)]['props']['className'] = current_classes + ' ' + a

        return tiles

    def update_placement(self, game_id: str, tiles: list[dict]) -> list[dict]:
        """ update the children of all tiles with the current game state"""
        for i, _ in enumerate(tiles):
            tiles[i]['props']['children'] = self.get_piece_asset(self.game(game_id).board.tile_by_index(i).piece)

        return tiles

    def update_tiles(
            self, game_id: str, tiles: list[dict], selected_tile_name: str, is_help_activated: bool
    ) -> list[dict]:
        """ update the tiles, update the placements and effects"""
        tiles = self.update_placement(game_id, tiles)
        tiles = self.reset_effects(tiles)

        # if there is a tile selected
        if selected_tile_name is not None:
            tiles = self.update_effects(game_id, tiles, selected_tile_name, add=['selected'])
            if is_help_activated:
                # id the valid moves
                for t in self.game(game_id).valid_moves(self.game(game_id).board.tile_by_name(selected_tile_name)):
                    tiles = self.update_effects(game_id, tiles, t.name, add=['valid-move'])

                threatened_tiles = [
                    t.name for t in self.game(game_id).is_under_thread_by(
                        self.game(game_id).board.tile_by_name(selected_tile_name)
                    )
                ]

                threatening_tiles = [
                    t.name for t in self.game(game_id).is_threatening(
                        self.game(game_id).board.tile_by_name(selected_tile_name)
                    )
                ]

                for t in set(threatened_tiles + threatening_tiles):
                    if t in threatened_tiles and t in threatening_tiles:
                        tiles = self.update_effects(game_id, tiles, t, add=['thrthr'])
                    elif t in threatened_tiles:
                        tiles = self.update_effects(game_id, tiles, t, add=['threatened'])
                    else:
                        tiles = self.update_effects(game_id, tiles, t, add=['threatening'])

        return tiles

    def update_selection(self, game_id: str, triggered_tile_name: str, selected_tile_name: str | None) -> str:
        """ update the selection state depending on which index was triggered. """
        # if nothing was selected and the player clicked on a piece of its own color, select it
        if selected_tile_name is None \
                and self.game(game_id).board.tile_by_name(triggered_tile_name).piece.color == self.game(game_id).turn:
            selected_tile_name = triggered_tile_name
        # if the click was on the currently already selected tile, deselect it
        elif triggered_tile_name == selected_tile_name:
            selected_tile_name = None
        elif triggered_tile_name != selected_tile_name and selected_tile_name is not None:
            selected_tile_name = triggered_tile_name
        else:
            pass

        return selected_tile_name

    def log(self, game_id: str, state: Optional[GameState], selected_tile_name: str):
        if selected_tile_name is not None:
            print(f"{game_id}: its {self.game(game_id).turn.name}'s turn, "
                  f"{self.game(game_id).board.tile_by_name(selected_tile_name).piece.__class__.__name__} at "
                  f"{selected_tile_name} is selected")
        else:
            print(f"{game_id}: its {self.game(game_id).turn.name}'s turn, nothing is selected")

        if state is not None:
            print(f'{game_id}: player {self.game(game_id).turn.name}: {state.name}')

    def get_piece_asset(self, piece: PieceType) -> Svg | None:
        """ loads the piece asset on <tile> and return as svg """
        return self.assets.get(str(piece))

    def callbacks(self):
        @self.callback(
            Output('chessboard', 'children'),
            Output('promotion', 'children'),
            Output('selected_tile_store', 'data'),
            Input({'type': 'tile', 'index': ALL}, 'n_clicks'),
            Input({'type': 'promotion', 'index': ALL}, 'n_clicks'),
            State('chessboard', 'children'),
            State('selected_tile_store', 'data'),
            State('help_store', 'data'),
            State('game_id_store', 'data'),
            prevent_initial_callback=True
        )
        def render(tile_clicks, promotion_clicks, tiles, selected_tile_name, is_help_activated, game_id):
            """ render a new frame of the game """
            _ = tile_clicks, promotion_clicks  # unused

            if ctx.triggered_id is None:
                raise PreventUpdate

            # check if a promotion event is ongoing
            promotion_tile = self.game(game_id).which_pawn_promotable()

            if self.game(game_id).state() == GameState.CHECKMATE \
                    or self.game(game_id).state() == GameState.OUT_OF_TIME:
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

                    game_state = None
                    if selected_tile_name is not None:
                        self.game(game_id).move(
                            self.game(game_id).board.tile_by_name(selected_tile_name),
                            self.game(game_id).board.tile_by_name(triggered_tile_name)
                        )

                        # check the game state after the move
                        game_state = self.game(game_id).state()

                        # deselect after move attempt
                        selected_tile_name = None
                    else:
                        # update which piece is selected
                        selected_tile_name = self.update_selection(game_id, triggered_tile_name, selected_tile_name)

                    self.log(game_id, game_state, selected_tile_name)

                    updated_tiles = self.update_tiles(game_id, tiles, selected_tile_name, is_help_activated)

                    # check if a promotion event is triggered
                    promotion_tile = self.game(game_id).which_pawn_promotable()

                    if promotion_tile is not None:
                        print('promotion event started')
                        return updated_tiles, self.init_promotion_tile(game_id, promotion_tile), selected_tile_name

                    # if not, finish regular turn
                    return updated_tiles, None, selected_tile_name

            # if clicked on a promotion tile
            elif ctx.triggered_id.get('type') == 'promotion':
                # promote the pawn to the selected type
                self.game(game_id).promote(
                    promotion_tile,
                    piece_type=PIECE_TYPE_MAPPER.get(
                        ctx.triggered_id.get('index')
                    )
                )
                print('promotion event finished')

                return (
                    self.update_tiles(game_id, tiles, selected_tile_name, is_help_activated),
                    None,
                    selected_tile_name
                )
            else:
                raise ValueError()

        @self.callback(
            Output('signal', 'className'),
            Input('chessboard', 'children'),
            Input('new_game_event_store', 'data'),
            Input('ticker', 'n_intervals'),
            State('game_id_store', 'data'),
            prevent_initial_call=True
        )
        def update_indicator(tile_click, new_game_click, time_tick, game_id):
            _ = tile_click, new_game_click, time_tick  # unused

            # threshold is set to 1 so the marker is updated at the next clock tick, when the clock is at 00:00
            threshold = 1

            # preventing update if the ticker triggers this callback but the player is not out of time,
            # so it doesn't calculate whether checkmate is reached every clock tick
            if ctx.triggered_id == 'ticker' and not self.game(game_id).out_of_time(threshold):
                raise PreventUpdate

            clss = ['signal']
            if self.game(game_id).turn == Color.BLACK:
                clss.append('move')
            if self.game(game_id).check():
                clss.append('check')
            if self.game(game_id).checkmate() or self.game(game_id).out_of_time(threshold):
                clss.append('checkmate')

            return ' '.join(clss)

        @self.callback(
            Output('app-container', 'children'),
            Output('game_id_store', 'data'),
            Output('new_game_event_store', 'data'),
            Input('game_id_store', 'data'),
            Input('new', 'n_clicks'),
            State('app-container', 'children'),
        )
        def start(game_id, _, app_elements):
            if ctx is None:
                raise PreventUpdate

            # init a new game
            _id = str(randint(1, 999_999_999)).zfill(9)

            if game_id is not None:
                print(f'{game_id}: starting new game with id: {_id} (active games: {len(self.games)})')
                self.games.pop(game_id)
                self.games |= {_id: Game()}
            else:
                self.games |= {_id: Game()}
                print(f'{_id}: starting new game (active games: {len(self.games)})')

            # reset the board and the clock
            for component, initializer in [
                ('chessboard', self.init_board),
                ('clocks', self.init_clocks)
            ]:
                [idx] = [app_elements.index(i) for i in app_elements if i['props']['id'] == component]
                app_elements[idx]['props']['children'] = [i.to_plotly_json() for i in initializer(_id)]

            return app_elements, _id, 'new_game_started'

        @self.callback(
            Output('help', 'className'),
            Output('help_store', 'data'),
            Input('help', 'n_clicks'),
            State('help_store', 'data'),
            prevent_initial_callback=True
        )
        def toggle_help(_, is_help_activated):
            if ctx.triggered_id is None:
                raise PreventUpdate

            # toggle help attr
            if is_help_activated:
                is_help_activated = False
                return 'help menu-item', is_help_activated

            is_help_activated = True
            return 'help menu-item on', is_help_activated

        @self.callback(
            Output('timer', 'className'),
            Output('clocks', 'className'),
            Output('ticker', 'disabled'),
            Output('timer_store', 'data'),
            Input('timer', 'n_clicks'),
            State('timer_store', 'data'),
            prevent_initial_callback=True
        )
        def toggle_timer(_, is_timer_activated):
            if ctx.triggered_id is None:
                raise PreventUpdate

            # toggle timer attr
            if is_timer_activated:
                is_timer_activated = False
                return 'timer menu-item', 'clocks', True, is_timer_activated

            is_timer_activated = True
            return 'timer menu-item on', 'clocks visible', False, is_timer_activated

        @self.callback(
            Output('white-clock', 'children'),
            Output('black-clock', 'children'),
            Input('ticker', 'n_intervals'),
            State('white-clock', 'children'),
            State('black-clock', 'children'),
            State('game_id_store', 'data'),
            prevent_initial_call=True
        )
        def tick_timer(_, white_time, black_time, game_id):
            if self.game(game_id).turn == Color.WHITE:
                self.game(game_id).update_player_time(Color.WHITE)
                return time_int_to_str(self.game(game_id).white.time), black_time

            self.game(game_id).update_player_time(Color.BLACK)
            return white_time, time_int_to_str(self.game(game_id).black.time)

        @self.callback(
            Output('unloader', 'id'),
            Input('unloader', 'close'),
            State('game_id_store', 'data'),
            prevent_initial_call=True
        )
        def remove_game_id_on_browser_refresh(_, game_id):
            print(f'{game_id}: closing game')
            self.games.pop(game_id)

            return 'listener'


if __name__ == '__main__':
    app = App()
    app.run(debug=True)
