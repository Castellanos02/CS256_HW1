from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    access = db.Column(db.Integer, nullable=False)

class github(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    stars = db.Column(db.String(100), unique=True, nullable=False)
    link = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="admin@gmail.com").first():
        default_user = User(name='Admin', email="admin@gmail.com", access=1)
        db.session.add(default_user)
        db.session.commit()
        

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search_engine')
def search():
    return render_template('search_engine.html')

@app.route('/repo_explorer')
def github():
    return render_template('repo_explorer.html')

@app.route('/bookmark')
def bookmark():
    return render_template('bookmark.html')

@app.route('/AI_chatot')
def bot():
    return render_template('AI_bot.html')

@app.route('/contribute')
def contribute():
    return render_template('contribute.html')

@app.route('/learning_material')
def learning():
    return render_template('learn_materials.html')


if __name__ == '__main__':
    app.run()