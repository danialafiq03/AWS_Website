from flask import Flask, render_template, url_for

application = Flask(__name__)
app = application

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
    app.run(host='0.0.0.0', port=8888)
