from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socket = SocketIO(app)

# Store usernames in memory (replace with a database)
logins = {'1': '0'}

# Store chat messages in memory (replace with a database)
messages = []

@app.route("/")
def index():
    return render_template('login.html')
@app.route("/chat")
def chat():
    return render_template('chat.html')


@socket.on('login')
def handle_login(data):
    username = data['username']
    password = data['password']
    login_status = False
    error = None
    if username not in logins:
        error = 'Invalid username'
    elif logins[username] != password:
        error = 'Invalid password'
    else:
        login_status = True
    emit('login', {'loginStatus': login_status, 'error': error})


@socket.on('join')
def join_room(data):
    #global username
    #username = data['username']
    print('join')
    return redirect('/chat')

@socket.on('message')
def handle_message(data):
    print(data['message'])
    message = data['message']
    username = 'username'
    messages.append({'username': username, 'message': message})
    emit('message', {'username': username, 'message': message})
    print('sent')


@socket.on('connect')
def handle_connect():
    print('User connected')


@socket.on('disconnect')
def handle_disconnect():
    print('User disconnected')


if __name__ == "__main__":
    socket.run(app, debug=True, allow_unsafe_werkzeug=True)
