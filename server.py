from bottle import route, run, Bottle, request, response, HTTPError
from enum import Enum, auto

app = Bottle()

games = {}


class Player(Enum):
    X = auto()
    O = auto()

    def __str__():
        self.name


class TicTacToePosition(Enum):
    TOP_LEFT = auto()
    TOP_MIDDLE = auto()
    TOP_RIGHT = auto()
    MIDDLE_LEFT = auto()
    MIDDLE_MIDDLE = auto()
    MIDDLE_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_MIDDLE = auto()
    BOTTOM_RIGHT = auto()

winning_conditions = [
    [TicTacToePosition.TOP_LEFT, TicTacToePosition.TOP_MIDDLE, TicTacToePosition.TOP_RIGHT],
    [TicTacToePosition.MIDDLE_LEFT, TicTacToePosition.MIDDLE_MIDDLE, TicTacToePosition.MIDDLE_RIGHT],
    [TicTacToePosition.BOTTOM_LEFT, TicTacToePosition.BOTTOM_MIDDLE, TicTacToePosition.BOTTOM_RIGHT],
    [TicTacToePosition.TOP_LEFT, TicTacToePosition.MIDDLE_LEFT, TicTacToePosition.BOTTOM_LEFT],
    [TicTacToePosition.TOP_MIDDLE, TicTacToePosition.MIDDLE_MIDDLE, TicTacToePosition.BOTTOM_MIDDLE],
    [TicTacToePosition.TOP_RIGHT, TicTacToePosition.MIDDLE_RIGHT, TicTacToePosition.BOTTOM_RIGHT],
    [TicTacToePosition.TOP_LEFT, TicTacToePosition.MIDDLE_MIDDLE, TicTacToePosition.BOTTOM_RIGHT],
    [TicTacToePosition.TOP_RIGHT, TicTacToePosition.MIDDLE_MIDDLE, TicTacToePosition.BOTTOM_LEFT]
    ]

class TicTacToe():
    def __init__(self):
        self.grid = {}
        self.winner = None

    def play_move(self, player, position):
        self.grid[position] = player
        if self.won():
            self.winner = player

    def won(self):
        global winning_conditions
        for cond in winning_conditions:
            if len(set([self.grid.get(pos, None) for pos in cond])) == 1:
                if self.grid.get(cond[0], None) is not None:
                    return True


@app.get('/')
def hello():
    return "Hi!"

@app.post('/tic-tac-toe')
def create_game():
    global games
    id = first_unused_id(games)
    games[id] = TicTacToe()
    return {'id': id}

@app.get('/tic-tac-toe/<id:int>')
def get_game(id):
    if game_does_not_exist(id):
        raise HTTPError(404)
    return {'id': id}

@app.put('/tic-tac-toe/<id:int>')
def play_move(id):
    if game_does_not_exist(id):
        raise HTTPError(404)
    global games
    game = games[id]
    game.play_move(Player[request.json['player']], TicTacToePosition[request.json['position']])
    if game.winner is None:
        winner = None
        game_over = False
    else:
        winner = game.winner.name
        game_over = True

    return {'id': id, 'winner': winner, 'game_over': game_over}

@app.delete('/tic-tac-toe/<id:int>')
def delete_game(id):
    if game_does_not_exist(id):
        raise HTTPError(404)
    global games
    del games[id]

def game_does_not_exist(id):
    global games
    return id not in games

def first_unused_id(dictionary):
    keys = dictionary.keys()
    return min(set(range(len(keys) + 1)) - set(keys))

if __name__ == '__main__':
    app.run(host='localhost', port='8080', debug=True)
