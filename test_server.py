import server
from webtest import TestApp, AppError
from pytest import raises


def test_says_hello():
    app = TestApp(server.app)
    server_response = app.get('/')
    assert server_response.text == 'Hi!'
    assert server_response.status_code == 200


def test_creates_games_with_incremental_ids():
    app =  TestApp(server.app)
    game_response = app.post('/tic-tac-toe')
    assert game_response.json == {'id': 0}
    assert game_response.status_code == 200

    game_response = app.post('/tic-tac-toe')
    assert game_response.json == {'id': 1}
    assert game_response.status_code == 200

def test_can_get_game_state():
    app =  TestApp(server.app)
    game_response = app.get('/tic-tac-toe/0')
    assert game_response.json == {'id': 0}
    assert game_response.status_code == 200

def test_can_make_move_on_game():
    app = TestApp(server.app)
    game_response = app.put('/tic-tac-toe/0', {'player': 'X', 'position': 'TOP_LEFT'})
    assert game_response.json == {'id': 0}
    assert game_response.status_code == 200

def test_can_delete_games():
    app = TestApp(server.app)
    game_response = app.delete('/tic-tac-toe/0')
    assert game_response.status_code == 200

def test_will_error_if_cannot_find_game_to_delete():
    app =  TestApp(server.app)
    game_response = app.delete('/tic-tac-toe/6', expect_errors=True)
    assert game_response.status_code == 404

def test_will_error_if_cannot_find_game():
    app =  TestApp(server.app)
    game_response = app.get('/tic-tac-toe/0', expect_errors=True)
    assert game_response.status_code == 404


def test_get_first_unused_id():
    assert server.first_unused_id({}) == 0
    assert server.first_unused_id({0: ''}) == 1
    assert server.first_unused_id({1: ''}) == 0
    assert server.first_unused_id({0: '', 2: ''}) == 1
