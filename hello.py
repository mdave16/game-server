from bottle import route, run, Bottle, request

app = Bottle()

game_counter = -1

@app.get('/')
def hello():
    return "Hi!"

@app.post('/tic-tac-toe')
def create_game():
    global game_counter
    game_counter += 1
    return {'id': game_counter}

@app.get('/tic-tac-toe/<id:int>')
def get_game(id):
    return {'id': id}

@app.put('/tic-tac-toe/<id:int>')
def play_move(id):
    print(request.json)
    return {'id': id}

if __name__ == '__main__':
    app.run(host='localhost', port='8080', debug=True)
