from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

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