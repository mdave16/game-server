from server import app, first_unused_id, TicTacToe, TicTacToePosition, Player, winning_conditions
from webtest import TestApp, AppError
from collections import OrderedDict

def test_says_hello():
    server_response = TestApp(app).get('/')
    assert server_response.text == 'Hi!'
    assert server_response.status_code == 200

def test_creates_games_with_incremental_ids():
    test_app = TestApp(app)
    game_response = test_app.post('/tic-tac-toe')
    assert game_response.json == {'id': 0}
    assert game_response
    game_response = test_app.post('/tic-tac-toe')
    assert game_response.json == {'id': 1}
    assert game_response.status_code == 200

def test_can_get_game_state():
    game_response = TestApp(app).get('/tic-tac-toe/0')
    assert game_response.json == {'id': 0}
    assert game_response.status_code == 200

def test_can_make_move_on_game():
    game_response = TestApp(app).put_json('/tic-tac-toe/0', {'player': 'X', 'position': 'TOP_LEFT'})
    assert game_response.json == {'id': 0}
    assert game_response.status_code == 200

def test_can_make_move_on_game():
    test_app = TestApp(app)
    test_app.put_json('/tic-tac-toe/0', {'player': 'X', 'position': 'TOP_LEFT'})
    test_app.put_json('/tic-tac-toe/0', {'player': 'X', 'position': 'TOP_MIDDLE'})
    game_response = test_app.put_json('/tic-tac-toe/0', {'player': 'X', 'position': 'TOP_RIGHT'})
    assert game_response.json == {'id': 0, 'winner': 'X', 'game_over': True}
    assert game_response.status_code == 200

def test_can_delete_games():
    game_response = TestApp(app).delete('/tic-tac-toe/0')
    assert game_response.status_code == 200

def test_will_error_if_cannot_find_game_to_delete():
    game_response = TestApp(app).delete('/tic-tac-toe/6', expect_errors=True)
    assert game_response.status_code == 404

def test_will_error_if_cannot_find_game():
    game_response = TestApp(app).get('/tic-tac-toe/0', expect_errors=True)
    assert game_response.status_code == 404

def test_get_first_unused_id():
    assert first_unused_id({}) == 0
    assert first_unused_id({0: ''}) == 1
    assert first_unused_id({1: ''}) == 0
    assert first_unused_id({0: '', 2: ''}) == 1

def test_tic_tac_toe():
    t = TicTacToe()
    assert t.grid == {}

    t.play_move(Player.X, TicTacToePosition.TOP_RIGHT)
    assert t.grid == {TicTacToePosition.TOP_RIGHT: Player.X}

def test_tic_tac_toe_win_conditions():
    global winning_conditions
    t = TicTacToe()
    for pos in winning_conditions[0]:
        t.play_move(Player.X, pos)
    assert t.winner == Player.X
