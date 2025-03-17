from flask import Flask, render_template, redirect, url_for, session, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import csv
from sqlalchemy.dialects.postgresql import UUID
import uuid
import openai


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'

db = SQLAlchemy(app)

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
    #image = db.Column(db.Integer, nullable=False)
    #skills = db.Column(db.String(100), nullable = False)

class blogs(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    mediaType = db.Column(db.String(100), nullable = False)
    #image = db.Column(db.Integer, nullable=False)

class openAi(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable = False)
    link = db.Column(db.String(200), nullable=False)
    mediaType = db.Column(db.String(100), nullable = False)
    #image = db.Column(db.Integer, nullable=False)

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
    #image = db.Column(db.Integer, nullable=False)

class udacity(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable = False)
    link = db.Column(db.String(200), nullable=False)
    stars = db.Column(db.Float, nullable=True)
    mediaType = db.Column(db.String(100), nullable = False)
    #image = db.Column(db.Integer, nullable=False)

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
    # id = db.Column(db.Integer, primary_key = True)
    # userId = db.Column(db.Integer, nullable=False)
    # mediaType = db.Column(db.String(100), nullable = False)
    # name = db.Column(db.String(100), nullable = False)
    # table = db.Column(db.String(100), nullable = False)

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
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    link = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    

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
                github_entry = githubdb(name=line[3],link=line[2],description=line[4],stars=int(line[5]), mediaType='Github Repo')
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

    client = OpenAI()
    chatHistory = {"user":""}

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
    bookmarked_items = bookmarked.query.filter_by(userId=session.get('user_id')).all()
    print(f"User ID: {session.get('user_id')}")  
    print(f"Bookmarked Items: {bookmarked_items}")  
    if not bookmarked_items:  
        print("No bookmarks found.")
    return render_template('home.html', is_admin=session.get('is_admin', 0))

@app.route('/search_engine', methods=['GET', 'POST'])
def search():
    tableMap = {"github" : githubdb, "papersWithCode" : papersWithCode, "udacity" : udacity,
                 "coursera" : coursera, "arxiv" : arxiv, "blogs" : blogs, "fastAi" : fastAi,
                   "openAi" : openAi, "documentation" : documentation, "googleScholar" : googleScholar}
    #poop
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

    print(media)

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

    return render_template('search_engine.html', results=queryResults, page=page, total_pages=total_pages, query=query, media=media, bookmarks=bookmarks, is_admin=session.get('is_admin', 0))

@app.route('/repo_explorer', methods=['GET','POST'])
def github():
    if 'bookmark' in request.form:
        bookmark = request.form.get("bookmark")
        bmId = uuid.UUID(request.form.get("id"))
        bmName = request.form.get("name")
        bmLink = request.form.get("link")
        bmDesc = request.form.get("description")
        if bookmark=='Bookmark':
            print("add")
            print(type(session['user_id']))
            bm_entry = bookmarked(mediaId=bmId, mediaType="Github Repo", name=bmName, userId=session['user_id'], link=bmLink, description=bmDesc, author=None)
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
    repos = db.session.query(githubdb).order_by(githubdb.stars.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('repo_explorer.html', repos=repos.items, pagination=repos, bookmarks=bookmarks, page=page, is_admin=session.get('is_admin', 0))

@app.route('/bookmark')
def bookmark():
    return render_template('bookmark.html',is_admin=session.get('is_admin', 0))

@app.route('/chatbot', methods=['GET','POST'])
def bot():
    # message = request.form['message']
    # chatHistory['user'] = "hi"
    # '''
    # response = client.responses.create(
    #     model="gpt-4o-mini",
    #     store=True,
    #     input=[
    #         {
    #             "role": "user",
    #             "content": "Hello, world!"}
    #     ]
    # )

    # print(response.output_text)'
    # '''
    # return render_template('AI_bot.html', chatHistory=chatHistory, is_admin=session.get('is_admin', 0))

    #     bot_reply = response.choices[0].message.content
    if "chat_history" not in session:
        session["chat_history"] = []  # Initialize chat history

    if request.method == 'POST':
        user_input = request.form['user_input']

        response = client.chat.completions.create(
            model="gpt-4",
            messages=session["chat_history"] + [{"role": "user", "content": user_input}]
        )

        bot_reply = response.choices[0].message.content

        # Store messages in session
        session["chat_history"].append({"role": "user", "content": user_input})
        session["chat_history"].append({"role": "assistant", "content": bot_reply})

        session.modified = True  # Ensure session updates are saved
    return render_template('AI_bot.html', chat_history=session["chat_history"])    
@app.route('/contribute', methods=["GET", "POST"])
def contribute():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        link = request.form.get("link")
        description = request.form.get("description")

        if not name or not email or not link or not description:
            flash("All fields are required!", "danger")
            return redirect("/")
        
        new_addition = paper_submission(name=name, email=email, link=link, description=description)
        db.session.add(new_addition)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('contribute.html',is_admin=session.get('is_admin', 0))

@app.route('/learning_material')
def learning():
    return render_template('learn_materials.html',is_admin=session.get('is_admin', 0))

@app.route('/approve')
def approve():
    if session.get('is_admin') != 1:
        return render_template('login.html')
    pending_submission = paper_submission.query.all()
    return render_template('approve_page.html',is_admin=session.get('is_admin', 0), pending_submission=pending_submission)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add_entry', methods=['POST'])
def add_entry():

    data = request.json
    print("Received data:", data)
    print("Session ID:", session.get('user_id'))
    # entry = bookmarked(userId=session.get('user_id'),link=data['link'], mediaType=data['mediaType'], author=data['author'], description=data.get("description"))
    if data['description']:
        entry = bookmarked(userId=session.get('user_id'),link=data['link'], mediaType=data['mediaType'], author=data['author'], description=data["description"])
    else:
        entry = bookmarked(userId=session.get('user_id'),link=data['link'], mediaType=data['mediaType'], author=data['author'], description="")
    print(entry)
    db.session.add(entry)
    db.session.commit()     

    return jsonify({"message": "Bookmark added successfully!"})  # No redirect!
    # return jsonify({"message": "Bookmark added successfully!"})


if __name__ == '__main__':
    app.run()