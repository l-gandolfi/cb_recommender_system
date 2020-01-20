# Information Retrieval 2019-2020
## Recommender System for News Tweets

- Luca Gandolfi 807485
- Bruno Palazzi 806908
- Stefano Sacco 807532

### Introduction
In this project we've developed a Content-base Filtering Recommender System with a Relevance Feedback updating system, for Tweets News.

### Instructions
First of all create a virtual environment: 
> python3 -m virtualenv ~/rs_venv

Then, clone our repository, and run:
> source rs_venv/bin/activate
>
> cd recommender-system
>
> pip3 install -r requirements.txt

Now the virtual environment is ready with all dependencies needed. <br>
To run the program now simply type:
> python3 gui.py

The Graphic User Interface will be loaded.

### Brief description
The data is loaded from a SQLite DataBase. This DB contains both the Users Profile and the Items Profile, where the Items are Tweet news. <br>
If you want to manage or just view the DB structure you can install SQLite:
> sudo apt-get install sqlite sqlitebrowser

The original Tweets were obtained by scraping using Twitter APi and stored into a .csv file. You don't need this csv file to use the program, but we leave it in the repository. <br>
In certain buttons there are ToolTip for the user, to clarify their functionalities. <br>
An in-depth description of this project can be read in the pdf file provided.

### Future releases
In the future releases, some updates will be performed: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - Remove the least performing model (i.e. only the BERT encoded model will be provided) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - Add a registration system and a login window