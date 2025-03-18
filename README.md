## CS 256 Homework


### Contributors 

    Castellanos02 - Axel Castellanos

    henry4912 - Henry Ha

#### How This Project Works

```
CS256 Homework.ipynb was created in Google Colab to gather data to store in our database. 
This involved using APIs for ArXiv, PapersWithCode, Github, etc. Resources that did not provide
 an API such as Coursera, FastAI, etc were webscraped for data. All data gathered through these
methods were stored on a SQLite database. We decided it would be easier to export all of the data
into csv files for us to process and store in another SQLite database in app.py.

requirements.txt are all of the packages required to run our project.

csvFiles contains all of the csv files holding data that we obtained through APIs and webscraping.

templates contains the html files that format each of our webpages.

app.py is the main file to run our project. It is responsible for setting up the SQLite database,
making queries to the database, sending results to the html files to display, and handling user
accounts.
```

#### Instructions to Use Project

1. Click this link in order to go our Heroku website https://homeworkcs2560-dfa3b6ca9d00.herokuapp.com/

2. In order to access our website, you will need to create an account

3. After creating account there are multiple tabs to view:
- Home (shows bookmarked items)
- Search Engine (leads to search bar)
- Github Repositories (lists trending github repositories)
- Submitted Material (shows the material a user submitted for approval)
- Chatbot (leads to a chatbot the user can interact with)
- Submit Material (leads to a page where the user can submit material in order for the admin to approve)
- AI Learning Materials (this shows a list of different materials in different categories for the topic of AI)
- Logout (this will log the user out)

4. If the user is an admin then they see another tab
- Admin Panel (this is where the admin can view submitted materials and approve or deny them)

5. In the Github Repositories and AI Learning Materials the user can bookmark pages they are interested in
