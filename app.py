from flask import Flask, render_template, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(100),unique=True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    access = db.Column(db.Integer, nullable=False)

class github(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    stars = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)

class arxiv(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)

class papersWithCode(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)

class coursera(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    stars = db.Column(db.String(100), nullable=False)
    #image = db.Column(db.Integer, nullable=False)
    #skills = db.Column(db.String(100), nullable = False)

class blogs(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    #image = db.Column(db.Integer, nullable=False)

class openAi(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    link = db.Column(db.String(200), nullable=False)
    #image = db.Column(db.Integer, nullable=False)

class googleScholar(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable = False)

class fastAi(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable = False)
    #image = db.Column(db.Integer, nullable=False)

class udacity(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    link = db.Column(db.String(200), nullable=False)
    stars = db.Column(db.String(100), nullable=True)
    #image = db.Column(db.Integer, nullable=False)

class documentation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    mediaType = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="admin@gmail.com").first():
        default_admin = User(user_name='admin', password='admin', email="admin@gmail.com", access=1)
        db.session.add(default_admin)
        db.session.commit()

        default_user = User(user_name='user',password='user', email="user@gmail.com", access=0)
        db.session.add(default_user)
        db.session.commit()     

    with open('csvFiles/arxiv.csv', 'r', encoding='utf-8') as f:
        csvFile = csv.reader(f)
        for line in csvFile:   
            arxiv_entry = arxiv(name=line[3],description=line[5],author=line[4],link=line[2])
            db.session.add(arxiv_entry)
            db.session.commit()   

    with open('csvFiles/blogs.csv', 'r', encoding='utf-8') as f:
        csvFile = csv.reader(f)
        for line in csvFile:   
            blog_entry = blogs(name=line[4],author=line[5],link=line[2])
            db.session.add(blog_entry)
            db.session.commit()  

    with open('csvFiles/coursera.csv', 'r', encoding='utf-8') as f:
        csvFile = csv.reader(f)
        for line in csvFile:   
            coursera_entry = coursera(name=line[4],author=line[5],link=line[3],stars=line[7])
            db.session.add(coursera_entry)
            db.session.commit()  

    with open('csvFiles/documentation.csv', 'r', encoding='utf-8') as f:
        csvFile = csv.reader(f)
        for line in csvFile:   
            doc_entry = documentation(name=line[3],author=line[4],link=line[2],mediaType=line[5])
            db.session.add(doc_entry)
            db.session.commit()  

    with open('csvFiles/fastai.csv', 'r', encoding='utf-8') as f:
        csvFile = csv.reader(f)
        for line in csvFile:   
            fastai_entry = fastAi(name=line[4],author=line[5],link=line[2],description=line[6])
            db.session.add(fastai_entry)
            db.session.commit()  
    
    with open('csvFiles/github.csv', 'r', encoding='utf-8') as f:
        csvFile = csv.reader(f)
        for line in csvFile:   
            github_entry = github(name=line[3],link=line[2],description=line[4],stars=line[5])
            db.session.add(github_entry)
            db.session.commit()  
    
    with open('csvFiles/googlescholar.csv', 'r', encoding='utf-8') as f:
        csvFile = csv.reader(f)
        for line in csvFile:   
            google_entry = googleScholar(name=line[3],link=line[2],description=line[5],author=line[4])
            db.session.add(google_entry)
            db.session.commit() 

    with open('csvFiles/openai.csv', 'r', encoding='utf-8') as f:
        csvFile = csv.reader(f)
        for line in csvFile:   
            openai_entry = openAi(name=line[4],link=line[2])
            db.session.add(openai_entry)
            db.session.commit() 

    with open('csvFiles/papersWithCode.csv', 'r', encoding='utf-8') as f:
        csvFile = csv.reader(f)
        for line in csvFile:   
            papers_entry = papersWithCode(name=line[3],link=line[2],description=line[5],author=line[4])
            db.session.add(papers_entry)
            db.session.commit() 

    with open('csvFiles/udacity.csv', 'r', encoding='utf-8') as f:
        csvFile = csv.reader(f)
        for line in csvFile:   
            udacity_entry = udacity(name=line[4],link=line[2],stars=line[5])
            db.session.add(udacity_entry)
            db.session.commit() 

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        user = User.query.filter_by(user_name=user_name, password=password).first()

        if user:
            session['user_id'] = user.id
            session['is_admin'] = user.access
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html', is_admin=session.get('is_admin', 0))

@app.route('/search_engine')
def search():
    return render_template('search_engine.html',is_admin=session.get('is_admin', 0))

@app.route('/repo_explorer')
def github():
    return render_template('repo_explorer.html',is_admin=session.get('is_admin', 0))

@app.route('/bookmark')
def bookmark():
    return render_template('bookmark.html',is_admin=session.get('is_admin', 0))

@app.route('/AI_chatot')
def bot():
    return render_template('AI_bot.html',is_admin=session.get('is_admin', 0))

@app.route('/contribute')
def contribute():
    return render_template('contribute.html',is_admin=session.get('is_admin', 0))

@app.route('/learning_material')
def learning():
    return render_template('learn_materials.html',is_admin=session.get('is_admin', 0))

@app.route('/approve')
def approve():
    if session.get('is_admin') != 1:
        return render_template('login.html')
    return render_template('approve_page.html',is_admin=session.get('is_admin', 0))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()