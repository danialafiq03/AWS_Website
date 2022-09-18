from flask import Flask, render_template, url_for, session, request, g, redirect
from flask_socketio import SocketIO, send
import random

application = Flask(__name__)
app = application
app.secret_key = 'secret123'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.before_request
def before_request():
    # if 'user_id' in session:
    #     try:
    #         db = shelve.open('register.db', 'r')
    #     except:
    #         db = shelve.open('register.db', 'c')
    #
    #     user_dict = db['Users']
    #     for key in user_dict:
    #         if key == session['user_id']:
    #             g.user = user_dict.get(key)
    #     db.close()
    # else:
    random_num = random.randint(0, 10000)
    session['guest_id'] = random_num

@socketio.on('message')
def handle_message(message):
    print("Received message: " + message)
    if message != "User connected!":
        send(message, broadcast=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return "Contact Page"

@app.route('/login')
def login():
    return "Login Page"

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8888, allow_unsafe_werkzeug=True)
