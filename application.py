from flask import Flask, render_template, url_for, session, request, g, redirect
from flask_socketio import SocketIO, send, emit
import random

application = Flask(__name__)
app = application
app.secret_key = 'secret123'
socketio = SocketIO(app, cors_allowed_origins="*")
usersList = []

@app.before_request
def before_request():
    if 'guest_id' in session:
        username = "Guest #" + str(session['guest_id'])
        g.user = {"username": username}

@socketio.on('message')
def handle_message(message):
    send(message, broadcast=True)

@socketio.on('connects')
def handle_connect(username):
    if username not in usersList:
        usersList.append(username)
    message = username + " connected!"
    emit('conn_message', message, broadcast=True)
    emit('users', usersList, broadcast=True)


@socketio.on('disconnect')
def disconnect_details():
    username = "Guest #" + str(session['guest_id'])
    print(f"{username} left the chat")
    usersList.remove(username)
    message = username + " left the chat"
    emit('disconn_message', message, broadcast=True)
    emit('users', usersList, broadcast=True)

@app.route('/')
def index():
    g.user = None
    if not session.get("guest_id") or session.get("user_id"):
        random_num = random.randint(0, 10000)
        session['guest_id'] = random_num
    if "guest_id" in session:
        g.user = {"username": "Guest #" + str(session['guest_id'])}
    elif "user_id" in session:
        g.user = {"username": str(session["user_id"])}
    return render_template('index.html')


@app.route('/contact')
def contact():
    return str(g.user['username'])


@app.route('/login')
def login():
    return "Login Page"

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=80, allow_unsafe_werkzeug=True)
