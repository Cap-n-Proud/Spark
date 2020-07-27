from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('yprh')
def handle_json(*yprh):
    print('received json: ' + str(yprh))


if __name__ == '__main__':
    socketio.run(app)
