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

1. Run the code in CS256 Homework.ipynb to gather data across all medias (This step can be skipped as the csv files are provided)

2. INSERT STEPS HERE TO DEPLOY PROJECT
