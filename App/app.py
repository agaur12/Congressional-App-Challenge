from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socket = SocketIO(app)

# Store chat messages in memory (replace with a database in a production app)
messages = []

@app.route("/")
def index():
   return render_template('index.html')

@socket.on('message')
def handle_message(data):
    print(data['message'])
    username = 'User1'  # You can replace this with the actual username
    message = data['message']
    messages.append({'username': username, 'message': message})
    emit('message', {'username': username, 'message': message}, broadcast=True)

@socket.on('connect')
def handle_connect():
    print('User connected')

@socket.on('disconnect')
def handle_disconnect():
    print('User disconnected')

if __name__ == "__main__":
    socket.run(app, debug=True, allow_unsafe_werkzeug=True)