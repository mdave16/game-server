from bottle import route, run, Bottle, request, response

app = Bottle()

games = {}

@app.get('/')
def hello():
    return "Hi!"

@app.post('/tic-tac-toe')
def create_game():
    global games
    id = first_unused_id(games)
    games[id] = {}
    return {'id': id}

@app.get('/tic-tac-toe/<id:int>')
def get_game(id):
    global games
    if id not in games:
        response.status = 404
        return
    return {'id': id}

@app.put('/tic-tac-toe/<id:int>')
def play_move(id):
    return {'id': id}

@app.delete('/tic-tac-toe/<id:int>')
def delete_game(id):
    global games
    if id not in games:
        response.status = 404
    else:
        del games[id]
    return

def first_unused_id(dictionary):
    keys = dictionary.keys()
    return min(set(range(len(keys) + 1)) - set(keys))

if __name__ == '__main__':
    app.run(host='localhost', port='8080', debug=True)
