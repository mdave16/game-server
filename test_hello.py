import hello
from webtest import TestApp


def test_says_hello():
    app = TestApp(hello.app)
    hello_response = app.get('/')
    assert hello_response.text == 'Hi!'
    assert hello_response.status_code == 200


def test_creates_games_with_incremental_ids():
    app =  TestApp(hello.app)
    game_response = app.post('/tic-tac-toe')
    assert game_response.json == {'id': 0}
    assert game_response.status_code == 200

    game_response = app.post('/tic-tac-toe')
    assert game_response.json == {'id': 1}
    assert game_response.status_code == 200

def test_can_get_game_state():
    app =  TestApp(hello.app)
    game_response = app.get('/tic-tac-toe/0')
    assert game_response.json == {'id': 0}
    assert game_response.status_code == 200
