from bottle import route, run, Bottle

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

if __name__ == '__main__':
    app.run(host='localhost', port='8080', debug=True)
