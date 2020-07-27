from flask import Flask, render_template
from flask_socketio import SocketIO
import socketio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

sio = socketio.Client()  # !!! at this point i receive a new connection on remote server, however the code freezes on this line and the script hang on until the end of the connection
sio = socketio.Connect('192.168.1.50', '54321')

@socketio.on('yprh')
def handle_json(*yprh):
    print('received json: ' + str(yprh))


if __name__ == '__main__':
    socketio.run(app)
