# sudo apt-get install python3 python-dev python3-dev \
#      build-essential libssl-dev libffi-dev \
#      libxml2-dev libxslt1-dev zlib1g-dev \
#      python-pip

import socketio

# standard Python
sio = socketio.Client()

@sio.event
def message(data):
    print('I received a message!')

@sio.on('CMDEcho')
def on_message(CMDEcho):
    print('I received a message!')
    print(CMDEcho)

@sio.on('yprh')
def print_data(*yprh):
        #print(str(yprh))
        print(yprh[3])
# def on_message(yprh):
#     print('I received a message!')
#     print(yprh)

@sio.event
def connect():
    print("I'm connected!")
    print('my sid is', sio.sid)
@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

sio.connect('http://192.168.1.50:54321')
sio.wait()
