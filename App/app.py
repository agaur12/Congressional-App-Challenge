from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit, send
from data import *
from translate import *

app = Flask(__name__)
socket = SocketIO(app)

# Store chat messages in memory (replace with a database)
messages = []
session = {'username': 'admin', 'language': 'en'}

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

@app.route("/")
def login():
    return render_template('login.html')


@app.route("/chat")
def chat():
    return render_template('chat.html')


@app.route("/register")
def register():
    return render_template('register.html')


@socket.on('register')
def handle_register(data):
    username = data['username']
    password = data['password']
    success, error = check_username(username, aws_access_key_id, aws_secret_access_key)
    if success:
        store_login_info(username, password, aws_access_key_id, aws_secret_access_key)
    emit('register', {'success': success, 'error': error})


@socket.on('login')
def handle_login(data):
    username = data['username']
    password = data['password']
    success, error = check_login_info(username, password, aws_access_key_id, aws_secret_access_key)
    if success:
        session['username'] = username
    emit('login', {'success': success, 'error': error})


@socket.on('language')
def select_language(data):
    session['language'] = str(data)

@socket.on('message')
def handle_message(data):
    username = session['username']
    message = data['message']
    language = session['language']
    messages.append({'username': username, 'message': message})
    translated_message = translate(language, message)
    emit('message', {'username': username, 'message': message, 'translated_message': translated_message})


@socket.on('connect')
def handle_connect():
    print('User connected')


@socket.on('disconnect')
def handle_disconnect():
    print('User disconnected')


if __name__ == "__main__":
    socket.run(app, debug=True, allow_unsafe_werkzeug=True)
