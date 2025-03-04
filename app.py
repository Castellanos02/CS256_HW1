from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask heroku app. Hello"

if __name__ == '__main__':
    app.run()