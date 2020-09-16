# GooBook
## a Web application and RESTful web service using Python/Flask

### Technologies Used:
- Python3
- Flask
- Sqlalchmey
- JSON
- Bootstrap
- Git
- SQL
- PostgreSQL
- azure app service

this is my Goobook web app and restful web service , a built from scratch project for the second assignment in the CS50w Course.

demo at: http://goobook.azurewebsites.net/  but my azure app service free plan will expire on 2/18/2019

The app name Goobook was inspired from the famouse search engine google.

When you sign up, will be able to search for books by isbn , title or author name, leave reviews for individual books, and see the reviews made by other people, as checking rating and reviews statistics coming from a third-party API by Goodreads.

The app it self has it's own API that users and developers can query for book details and book reviews programmatically . i wrote a page where you can read about it's usage.

### big notes:
DATABASE_URL variable need to be in the environment with valid database URI. also goodreads api need to fill in config file (development.py or production.py)

### notes :
#### Registration :
  - username : i decided to let signup/login use (email address as a user name). people tend to forget the username more than they would forget thier email address.
  - password : also password should be at least 8 or char, and have at least one capital letter , on small letter and a one digit. this done in front end using html5 pattren tag and regex. To DO: adding back-end validition.
#### login:
at login we i decided to record the time user loged in in last seen column in users table, so maybe it help later to check for unactive users.
#### import:
i was confused about if this program should create the actual db from scratch or just import the csv into it. i decided to make the import program only able to impprt the csv if the db was init with the correct tables, else it will tell to run db_init program. (another program i wrote to create the actual tables from schema.sql file.)

in the import program i made it posible two import the csv file into the db using one of two methods. one using postgresql native import (copy command), and one using isert statment. the native import is the defult when you run the import program . it take only seconds. type `import.py -h` for info.

#### Search:
i made some addition to the basic requirements, included pagination in search results.

how pagination had been implemented? using sql LIMIT and OFFSET in the back-end with a help of dynamic url for next and prev page made using jinja.
#### Book Page:
also in book page, i added a book cover img using cover third-party API by openlibrary.org. it was easy to add using jinja template alone.

https://openlibrary.org/dev/docs/api/covers

#### Review Submission:
review submission form was made using Bootstrap's JavaScript modal plugin. as login and signup forms. to improve the UX.
#### Goodreads Review Data:
statistics data from goodreads was included in the book page with a ref note to goodreads website.
#### API Access:
included as project requirements. nothing less, nothing more..
   
Beyond assignment(project) requirements, i added few dditional views.
- MyBooks Page: users will be taken to a page where they can see all the reviews they submited before with links to the reviewd books.
- API Page: just a pge with the instruction required for using the app API.

outside the main Application i made two additional programs:
- db_init.py : this will read the schema.sql file and execute it to create the tables in the db. you can type `db_init.py -h` for more help about using this app as i packed it with extra functionlty to help me while i develop this app, for example `db_init.py -r` will drop the tables in the db and create all tables again, helps me when i decede to change some columns in the db and want to start over.
- run.py : this will activte the app virual env located in app folder/venv , and lunch the flask app in host:0.0.0.0


### special note:
sqlalchmey db engine and the db scoped session come from db_helper.py module.

basicly the application.py , the import.py program and db_init.py program use the engine and session from db_helper module by importing it.

### summary:

    applicatio FOLDER
        db_init.py      program to create the db tables from schema.sql file.
                        see: db_init.py -h
        import.py       program to import the books.csv into PostgreSQL database.
                        see: import.py -h
        db_helper.py    module conatins database access layer
        db_functions.py module contains functions deal with the database
        application.py  the web application
        run.py          just shortcut to activate the app virtual env and run app
        schema.sql      sql file contains db schema (users, books, reviews)
        books.csv       
        requirements.txt
        README.md       this file
        venv FOLDER     i didn't submit it, this contain virtual env for this app
        templates FOLDER  my jinja templates.
            api.html    child template : a page descripe the app API usage.
            base.html   the base template. contains header, footer, nav, Bs scripts
            details.html child template : a pgae display the book details.
            index.html  child template : the home page.
            mybooks.html child template : a pgae to show the user his own reviews.
            results.html child template : display the search results.
        static FOLDER    contain css file , some left empty, for later.
            api.css
            cover.css
            details.css
            mybooks.css
            results.css
        instance FOLDER
            config.py    should contain any secret config
        config FOLDER    this is a package contain spicific env config fils
            development.py  settings you want to apply when in development env
            production.py   settings you wnat to apply when in production env
