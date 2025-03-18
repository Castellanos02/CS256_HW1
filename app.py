from flask import Flask, render_template, redirect, url_for, session, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import csv
from sqlalchemy.dialects.postgresql import UUID
import uuid
import openai
import requests


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = 'your_secret_key_here'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'


db = SQLAlchemy(app)

'''
Database Tables:
'''

class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    user_name = db.Column(db.String(100),unique=True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    access = db.Column(db.Integer, nullable=False)

class githubdb(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    stars = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String(200), nullable=False)
    mediaType = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(100), nullable=True)

class arxiv(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    mediaType = db.Column(db.String(100), nullable = False)

class papersWithCode(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    mediaType = db.Column(db.String(100), nullable = False)

class coursera(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    stars = db.Column(db.Float, nullable=False)
    mediaType = db.Column(db.String(100), nullable = False)

class blogs(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    mediaType = db.Column(db.String(100), nullable = False)

class openAi(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable = False)
    link = db.Column(db.String(200), nullable=False)
    mediaType = db.Column(db.String(100), nullable = False)

class googleScholar(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable = False)
    mediaType = db.Column(db.String(100), nullable = False)

class fastAi(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable = False)
    mediaType = db.Column(db.String(100), nullable = False)

class udacity(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable = False)
    link = db.Column(db.String(200), nullable=False)
    stars = db.Column(db.Float, nullable=True)
    mediaType = db.Column(db.String(100), nullable = False)

class documentation(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    mediaType = db.Column(db.String(100), nullable=False)

class allMedia(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    mediaId = db.Column(UUID(as_uuid=True))
    mediaType = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100), nullable = False)
    table = db.Column(db.String(100), nullable = False)

class bookmarked(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(UUID(as_uuid=True))
    mediaId = db.Column(UUID(as_uuid=True))
    name = db.Column(db.String(100), nullable = False)
    link = db.Column(db.String(100), nullable=False)
    mediaType = db.Column(db.String(100), nullable = False)
    stars = db.Column(db.Float, nullable=True)
    author = db.Column(db.String(100), nullable = True)
    description = db.Column(db.String(200), nullable = False)

class paper_submission(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(UUID(as_uuid=True))
    name = db.Column(db.String(100), nullable = False)
    paper_title = db.Column(db.String(200), nullable = False)
    link = db.Column(db.String(100), nullable = False)
    authors = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable = False)
    approved = db.Column(db.String(100), nullable=False)
    
'''
Once app initiates, database creates tables and places a user and admin account into the User table
Also checks if the arxiv database table is populated. If not, it will read all the csv files to
populate all database tables.
'''

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="admin@gmail.com").first():
        default_admin = User(user_name='admin', password='admin', email="admin@gmail.com", access=1)
        db.session.add(default_admin)
        db.session.commit()

        default_user = User(user_name='user',password='user', email="user@gmail.com", access=0)
        db.session.add(default_user)
        db.session.commit()     

    if not db.session.query(arxiv).first():
        with open('csvFiles/arxiv.csv', 'r', encoding='utf-8') as f:
            csvFile = csv.reader(f)
            skipHeader = 1
            for line in csvFile:
                if skipHeader:
                    skipHeader = 0
                    continue
                arxiv_entry = arxiv(name=line[3],description=line[5],author=line[4],link=line[2], mediaType='Research')
                db.session.add(arxiv_entry)
                db.session.commit()   
        arxivEntries = db.session.query(arxiv).all()
        for i in arxivEntries:
            media_entry = allMedia(mediaId=i.id, mediaType="Research", name=i.name, table='arxiv')
            db.session.add(media_entry)
            db.session.commit()  

        with open('csvFiles/blogs.csv', 'r', encoding='utf-8') as f:
            csvFile = csv.reader(f)
            skipHeader = 1
            for line in csvFile:
                if skipHeader:
                    skipHeader = 0
                    continue   
                blog_entry = blogs(name=line[4],author=line[5],link=line[2], mediaType='Blog')
                db.session.add(blog_entry)
                db.session.commit()  
        blogsEntries = db.session.query(blogs).all()
        for i in blogsEntries:
            media_entry = allMedia(mediaId=i.id, mediaType="Blogs", name=i.name, table='blogs')
            db.session.add(media_entry)
            db.session.commit()  

        with open('csvFiles/coursera.csv', 'r', encoding='utf-8') as f:
            csvFile = csv.reader(f)
            skipHeader = 1
            for line in csvFile:
                if skipHeader:
                    skipHeader = 0
                    continue   
                coursera_entry = coursera(name=line[4],author=line[5],link=line[3],stars=float(line[7]), mediaType='Course')
                db.session.add(coursera_entry)
                db.session.commit()  
        courseraEntries = db.session.query(coursera).all()
        for i in courseraEntries:
            media_entry = allMedia(mediaId=i.id, mediaType="Course", name=i.name, table='coursera')
            db.session.add(media_entry)
            db.session.commit()  

        with open('csvFiles/documentation.csv', 'r', encoding='utf-8') as f:
            csvFile = csv.reader(f)
            skipHeader = 1
            for line in csvFile:
                if skipHeader:
                    skipHeader = 0
                    continue   
                doc_entry = documentation(name=line[3],author=line[4],link=line[2],mediaType=line[5])
                db.session.add(doc_entry)
                db.session.commit()  
        docEntries = db.session.query(documentation).all()
        for i in docEntries:
            media_entry = allMedia(mediaId=i.id, mediaType="Documentation", name=i.name, table='documentation')
            db.session.add(media_entry)
            db.session.commit()  

        with open('csvFiles/fastai.csv', 'r', encoding='utf-8') as f:
            csvFile = csv.reader(f)
            skipHeader = 1
            for line in csvFile:
                if skipHeader:
                    skipHeader = 0
                    continue   
                fastai_entry = fastAi(name=line[4],author=line[5],link=line[2],description=line[6], mediaType='Blog')
                db.session.add(fastai_entry)
                db.session.commit()  
        fastEntries = db.session.query(fastAi).all()
        for i in docEntries:
            media_entry = allMedia(mediaId=i.id, mediaType="Blogs", name=i.name, table='fastAi')
            db.session.add(media_entry)
            db.session.commit()  
        
        with open('csvFiles/github.csv', 'r', encoding='utf-8') as f:
            csvFile = csv.reader(f)
            skipHeader = 1
            for line in csvFile:
                if skipHeader:
                    skipHeader = 0
                    continue   
                github_entry = githubdb(name=line[3],link=line[2],description=line[4],stars=int(line[5]), mediaType='Github Repo', author=line[6], language=line[7])
                db.session.add(github_entry)
                db.session.commit()  
        githubEntries = db.session.query(githubdb).all()
        for i in githubEntries:
            media_entry = allMedia(mediaId=i.id, mediaType="Github Repo", name=i.name, table='github')
            db.session.add(media_entry)
            db.session.commit() 
        
        with open('csvFiles/googlescholar.csv', 'r', encoding='utf-8') as f:
            csvFile = csv.reader(f)
            skipHeader = 1
            for line in csvFile:
                if skipHeader:
                    skipHeader = 0
                    continue   
                google_entry = googleScholar(name=line[3],link=line[2],description=line[5],author=line[4], mediaType='Research')
                db.session.add(google_entry)
                db.session.commit() 
        googleEntries = db.session.query(googleScholar).all()
        for i in googleEntries:
            media_entry = allMedia(mediaId=i.id, mediaType="Research", name=i.name, table='googleScholar')
            db.session.add(media_entry)
            db.session.commit() 

        with open('csvFiles/openai.csv', 'r', encoding='utf-8') as f:
            csvFile = csv.reader(f)
            skipHeader = 1
            for line in csvFile:
                if skipHeader:
                    skipHeader = 0
                    continue   
                openai_entry = openAi(name=line[4],link=line[2], mediaType='Blog')
                db.session.add(openai_entry)
                db.session.commit() 
        openEntries = db.session.query(openAi).all()
        for i in openEntries:
            media_entry = allMedia(mediaId=i.id, mediaType="Blogs", name=i.name, table='openAi')
            db.session.add(media_entry)
            db.session.commit() 

        with open('csvFiles/papersWithCode.csv', 'r', encoding='utf-8') as f:
            csvFile = csv.reader(f)
            skipHeader = 1
            for line in csvFile:
                if skipHeader:
                    skipHeader = 0
                    continue   
                papers_entry = papersWithCode(name=line[3],link=line[2],description=line[5],author=line[4], mediaType='Research')
                db.session.add(papers_entry)
                db.session.commit() 
        papersEntries = db.session.query(papersWithCode).all()
        for i in papersEntries:
            media_entry = allMedia(mediaId=i.id, mediaType="Research", name=i.name, table='papersWithCode')
            db.session.add(media_entry)
            db.session.commit() 

        with open('csvFiles/udacity.csv', 'r', encoding='utf-8') as f:
            csvFile = csv.reader(f)
            skipHeader = 1
            for line in csvFile:
                if skipHeader:
                    skipHeader = 0
                    continue
                star = 0
                if line[5] != 'null':
                    star = float(line[5])
                else:
                    star = None
                udacity_entry = udacity(name=line[4],link=line[2],stars=star, mediaType='Course')
                db.session.add(udacity_entry)
                db.session.commit()
        udacityEntries = db.session.query(udacity).all()
        for i in udacityEntries:
            media_entry = allMedia(mediaId=i.id, mediaType="Course", name=i.name, table='udacity')
            db.session.add(media_entry)
            db.session.commit()

'''
Allows registered users to log in
'''
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

'''
Displays all of the items that the user has bookmarked. Handles unbookmarking items
in the home page.
'''
@app.route('/home', methods=['GET','POST'])
def home():
    if 'bookmark' in request.form:
        bookmark = request.form.get("bookmark")
        bmId = uuid.UUID(request.form.get("id"))
        if bookmark=='Bookmark':
            print('add')
            bmName = request.form.get("name")
            bmAuthor = request.form.get("author")
            bmStars = request.form.get("stars")
            if bmStars and bmStars != "None":
                bmStars = float(bmStars)
            else:
                bmStars = None
            bmMedia = request.form.get("mediaType")
            bmLink = request.form.get("link")
            bmDesc = request.form.get("description")
            bm_entry = bookmarked(mediaId=bmId, mediaType=bmMedia, name=bmName, userId=session['user_id'], link=bmLink, description=bmDesc, author=bmAuthor, stars=bmStars)
            db.session.add(bm_entry)
            db.session.commit()
        else:
            print("delete")
            remove = db.session.query(bookmarked).filter(bookmarked.mediaId==bmId, bookmarked.userId==session['user_id']).first()
            print(remove)
            if remove:
                print("in")
                db.session.delete(remove)
                db.session.commit()
    bookmarked_items = bookmarked.query.filter_by(userId=session.get('user_id')).all()
    bookmarks = db.session.query(bookmarked.mediaId).filter(bookmarked.userId==session.get('user_id')).all()
    bookmarks = [str(i[0]) for i in bookmarks]

    print(f"User ID: {session.get('user_id')}")  
    print(f"Bookmarked Items: {bookmarked_items}")  
    if not bookmarked_items:  
        print("No bookmarks found.")
    return render_template('home.html', bookmarked_items=bookmarked_items, bookmarks=bookmarks, is_admin=session.get('is_admin', 0))

'''
Creates a new account for the user to use the website
'''
@app.route('/create_user', methods=['GET', 'POST'])
def create():
    error=None
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        email = request.form['email']
        existing_user = User.query.filter((User.user_name == user_name) | (User.email == email)).first()
        if existing_user:
            if existing_user.user_name == user_name and existing_user.email == email:
                error = "Username and Email already in use"
            elif existing_user.email == email:
                error = "Email already in use"
            elif existing_user.user_name == user_name:
                error = "Username already in use"
        else:
            new_user = User(user_name=user_name, password=password, email=email, access=0)
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            session['is_admin'] = new_user.access
            return redirect(url_for('home'))
    return render_template('create_user.html', error=error)

'''
Creates a search engine using Google API. The user can use this to get material based on the input they provide. The user can filter what type of category they want. 
'''
@app.route('/search_engine', methods=['GET', 'POST'])
def search():
    query = request.form.get("query")
    category = request.form.get("category")
    results = []

    if query:
        if category == "tutorial":
            query += " AI tutorial"
        elif category == "research":
            query += " AI research paper site:arxiv.org OR site:researchgate.net OR site:scholar.google.com"
        elif category == "github":
            query += " AI site:github.com"
        elif category == "course":
            query += " AI course site:coursera.org OR site:udemy.com OR site:edx.org"
        elif category == "blog":
            query += " AI blog site:medium.com OR site:dev.to OR site:towardsdatascience.com"

        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
        response = requests.get(url).json()
        results = response.get("items", [])

    return render_template("search.html", results=results)

'''
Displays trending AI Github repositories. Allows users to bookmark/unbookmark
Github repositories.
'''
@app.route('/repo_explorer', methods=['GET','POST'])
def github():
    if 'bookmark' in request.form:
        bookmark = request.form.get("bookmark")
        bmId = uuid.UUID(request.form.get("id"))
        bmName = request.form.get("name")
        bmLink = request.form.get("link")
        bmAuthor = request.form.get("author")
        bmStars = request.form.get("stars")
        bmDesc = request.form.get("description")
        if bookmark=='Bookmark':
            print("add")
            print(type(session['user_id']))
            bm_entry = bookmarked(mediaId=bmId, mediaType="Github Repo", name=bmName, userId=session['user_id'], link=bmLink, description=bmDesc, author=bmAuthor, stars=bmStars)
            db.session.add(bm_entry)
            db.session.commit()
        else:
            print("delete")
            remove = db.session.query(bookmarked).filter(bookmarked.mediaId==bmId, bookmarked.userId==session['user_id']).first()
            print(remove)
            if remove:
                print("in")
                db.session.delete(remove)
                db.session.commit()

    bookmarks = db.session.query(bookmarked.mediaId).filter(bookmarked.userId==session['user_id']).all()
    bookmarks = [i[0] for i in bookmarks]
    page = request.args.get('page', 1, type=int)
    repos = db.session.query(githubdb).order_by(githubdb.stars.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('repo_explorer.html', repos=repos.items, pagination=repos, bookmarks=bookmarks, page=page, is_admin=session.get('is_admin', 0))

'''
Displays the items a user submitted for approval
'''
@app.route('/submitted_report')
def submitted():
    submitted_items = paper_submission.query.filter_by(user_id=session.get('user_id')).all()
    print(f"User ID: {session.get('user_id')}")
    print(f"Bookmarked Items: {submitted_items}")   
    if not submitted_items:
        print("No items found.") 
    return render_template('submitted_work.html',is_admin=session.get('is_admin', 0), submitted_items=submitted_items)

'''
Allows the user to delete any papers they submitted
'''
@app.route('/delete_paper/<int:paper_id>', methods=['POST'])
def delete_paper(paper_id):
    paper = paper_submission.query.get(paper_id)

    db.session.delete(paper)
    db.session.commit()

    return redirect(url_for('submitted'))
'''
Allows the admin to make a decision on the items users submit
'''
@app.route('/paper_decision/<int:paper_id>/<string:decision>', methods=['POST'])
def paper_decision(paper_id, decision):
    paper = paper_submission.query.get(paper_id)
    paper.approved = decision
    db.session.commit()

    return redirect(url_for('approve'))    

'''
Allows the user to interact with a chatbot with the OpenAI API
'''
@app.route('/chatbot', methods=['GET','POST'])
def bot():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == 'POST':
        user_input = request.form['user_input']

        response = client.chat.completions.create(
            model="gpt-4",
            messages=session["chat_history"] + [{"role": "user", "content": user_input}]
        )

        bot_reply = response.choices[0].message.content

        session["chat_history"].append({"role": "user", "content": user_input})
        session["chat_history"].append({"role": "assistant", "content": bot_reply})

        session.modified = True
    return render_template('AI_bot.html', is_admin=session.get('is_admin', 0),chat_history=session["chat_history"])   

'''
Allows the user to submit a new research paper into the database
''' 
@app.route('/contribute', methods=["GET", "POST"])
def contribute():
    error_message=None
    if request.method == "POST":
        user_id = session.get('user_id')
        name = request.form.get("name")
        paper_title = request.form.get('paper_title')
        link = request.form.get("link")
        authors = request.form.get("authors")
        description = request.form.get("description")
        approved = "Waiting Approval"

        if not name or not paper_title or not link or not authors or not description:
            flash("All fields are required!", "danger")
            return redirect("/")
        
        existing_paper = paper_submission.query.filter((paper_submission.paper_title == paper_title) | (paper_submission.link == link)).first()

        if existing_paper:
            error_message = "A paper with this title or link already exists!"
            return render_template('contribute.html', is_admin=session.get('is_admin', 0), error_message=error_message)

        
        new_addition = paper_submission(user_id=user_id,name=name, paper_title=paper_title, link=link, authors=authors, description=description, approved=approved)
        db.session.add(new_addition)
        db.session.commit()

        return redirect(url_for('submitted'))

    return render_template('contribute.html', is_admin=session.get('is_admin', 0), error_message=error_message)

'''
Displays data stored in the database for the user including research papers, 
github repositories, courses, blogs, etc. Allows user to search for specific queries
and filter specific media types.
'''
@app.route('/learning_material', methods=['GET','POST'])
def learning():
    tableMap = {"github" : githubdb, "papersWithCode" : papersWithCode, "udacity" : udacity,
                 "coursera" : coursera, "arxiv" : arxiv, "blogs" : blogs, "fastAi" : fastAi,
                   "openAi" : openAi, "documentation" : documentation, "googleScholar" : googleScholar}
    
    if 'bookmark' in request.form:
        bookmark = request.form.get("bookmark")
        bmId = uuid.UUID(request.form.get("id"))
        if bookmark=='Bookmark':
            print('add')
            bmName = request.form.get("name")
            bmAuthor = request.form.get("author")
            bmStars = request.form.get("stars")
            if bmStars:
                bmStars = float(bmStars)
            else:
                bmStars = None
            bmMedia = request.form.get("mediaType")
            bmLink = request.form.get("link")
            bmDesc = request.form.get("description")
            bm_entry = bookmarked(mediaId=bmId, mediaType=bmMedia, name=bmName, userId=session['user_id'], link=bmLink, description=bmDesc, author=bmAuthor, stars=bmStars)
            db.session.add(bm_entry)
            db.session.commit()
        else:
            print("delete")
            remove = db.session.query(bookmarked).filter(bookmarked.mediaId==bmId, bookmarked.userId==session['user_id']).first()
            print(remove)
            if remove:
                print("in")
                db.session.delete(remove)
                db.session.commit()

    bookmarks = db.session.query(bookmarked.mediaId).filter(bookmarked.userId==session['user_id']).all()
    bookmarks = [i[0] for i in bookmarks]
    print(bookmarks)
    
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)
    media = request.args.get('media')

    emptyQ = False
    if query == '':
        emptyQ = True

    if media == 'All' and emptyQ:
        results = db.session.query(allMedia).all()
    elif media == 'All':
        results = db.session.query(allMedia).filter(allMedia.name.ilike(f'%{query}%')).all()
    elif media != 'All' and not emptyQ:
        results = db.session.query(allMedia).filter(allMedia.name.ilike(f'%{query}%'), allMedia.mediaType==media).all()
    else:
        results = db.session.query(allMedia).filter(allMedia.mediaType==media).all()

    queryResults = []

    for i in results:
        r = db.session.query(tableMap[i.table]).filter(tableMap[i.table].id==i.mediaId)
        all_r = r.all()
        if len(all_r) > 0:
            queryResults.append(all_r[0])

    total_pages = (len(queryResults) // 12) + (1 if len(queryResults) % 12 > 0 else 0)
    start = (page - 1) * 12
    end = start + 12
    queryResults = queryResults[start:end]
    
    return render_template('learn_materials.html', results=queryResults, page=page, total_pages=total_pages, query=query, media=media, bookmarks=bookmarks, is_admin=session.get('is_admin', 0))

'''
Allows admins to approve research papers submitted by users
'''
@app.route('/approve')
def approve():
    if session.get('is_admin') != 1:
        return render_template('login.html')
    pending_submission = paper_submission.query.all()
    return render_template('approve_page.html',is_admin=session.get('is_admin', 0), pending_submission=pending_submission)

'''
Allows users to log out of their account
'''
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add_entry', methods=['POST'])
def add_entry():

    data = request.json
    print("Received data:", data)
    print("Session ID:", session.get('user_id'))
    if data['description']:
        entry = bookmarked(userId=session.get('user_id'),link=data['link'], mediaType=data['mediaType'], author=data['author'], description=data["description"])
    else:
        entry = bookmarked(userId=session.get('user_id'),link=data['link'], mediaType=data['mediaType'], author=data['author'], description="")
    print(entry)
    db.session.add(entry)
    db.session.commit()     

    return jsonify({"message": "Bookmark added successfully!"}) 


if __name__ == '__main__':
    app.run()