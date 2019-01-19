# © 2019 Sameh Farouk Abouel Saad.

import os
import requests
from flask import (Flask, session, render_template, request, url_for, flash,
                   redirect, jsonify)
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from db_functions import (register_this_user, get_user_by_email,
                       update_user_last_seen, search_for_books, get_book_by_isbn,
                       submit_this_review, check_can_submit, get_book_reviews, get_user_reviews)
from functools import wraps

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.development')
app.config.from_pyfile('config.py', silent=True)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure flask_bcrypt
f_bcrypt = Bcrypt(app)

# Set up database
#engine = create_engine(DATABASE_URL)
#db = scoped_session(sessionmaker(bind=engine))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            flash("please log in first to get access to thousands of books's information")
            return redirect(url_for('home', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/search')
@login_required
def search():
    searchword = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    if searchword:
        # do the search
        matched_by_title, matched_by_author, matched_by_isbn = search_for_books(
            searchword, page=page)
    return render_template("results.html", matched_by_title=matched_by_title,
                           matched_by_author=matched_by_author, matched_by_isbn=matched_by_isbn, page=page)


@app.route('/login', methods=['POST'])
def logIn():
    # do the login
    userEmail = request.form.get('email')
    _password = request.form.get('password')
    r = get_user_by_email(userEmail)
    if r:
        # check the password
        if f_bcrypt.check_password_hash(bytes(r.password), _password):
            session['user_id'] = r.id
            session['user_name'] = r.name
            # update last seen
            update_user_last_seen(session['user_id'])
            return redirect(url_for('home'))
        else:
            flash('wrong password')
    else:
        flash('email not found')
    return redirect(url_for('home'))


@app.route('/signup', methods=['POST'])
def signUp():
    # get user info from the form
    userName = request.form.get('name')
    userEmail = request.form.get('email')
    _password = request.form.get('password')
    # TO DO (vaildate user mail info)
    # ______
    password_hash = f_bcrypt.generate_password_hash(_password)
    # register the user
    r = register_this_user(userName, userEmail, password_hash)
    if r:
        session['user_id'] = r.id
        session['user_name'] = r.name
        flash('you were registered')
        return redirect(url_for('home'))
    else:
        flash('failed to register the user. email already exeists')
        return redirect(url_for('home'))


@app.route('/book/<isbn>')
@login_required
def bookDetails(isbn):
    book = get_book_by_isbn(isbn)
    if not book:
        return 'isbn not found!', 404
    else:
        goodreads_info = get_book_from_goodreads_api(isbn)
        submit = check_can_submit(book['id'], session['user_id'])
        reviews = get_book_reviews(book['id'])
        return render_template("details.html", book=book, goodreads_info=goodreads_info, submit=submit, reviews=reviews)


@app.route('/api/<isbn>')
def api(isbn):
    book = get_book_by_isbn(isbn)
    if not book:
        return 'isbn not found!', 404
    else:
        goodreads_info = get_book_from_goodreads_api(isbn)
        api_dic = {"title": book['title'], "author": book['author'], "year": book['publication_year'],
                   "isbn": book['isbn'], "review_count": goodreads_info['books'][0]['work_reviews_count'],
                   "average_score": float(goodreads_info['books'][0]['average_rating'])}

        return jsonify(api_dic)


@app.route('/api')
@login_required
def apiUsage():
    return render_template('api.html')


@app.route('/mybooks')
@login_required
def myBooks():
    page = int(request.args.get('page', 1))
    mybooks = get_user_reviews(session['user_id'], page)
    return render_template('mybooks.html', mybooks=mybooks, page=page)


@app.route('/logOut')
@login_required
def logOut():
    # do the logout
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('you were loged out')
    return redirect(url_for('home'))


@app.route('/submit', methods=['POST'])
@login_required
def submitReview():
    # get user info from the form
    rate = request.form.get('rate')
    review = request.form.get('review')
    book_id = request.form.get('bookId')
    # TO DO (vaildate user info)
    # ______
    # register the user
    r = submit_this_review(rate, review, session['user_id'], book_id)
    if r:
        flash(f'your review have been submited')
        return redirect(request.referrer)
    else:
        flash('failed to submit the review.')
        return redirect(request.referrer)


def get_book_from_goodreads_api(isbn):
    key = app.config.get('GOODREADS_API_KEY')
    if key:
        try:
            res = requests.get("https://www.goodreads.com/book/review_counts.json",
                               params={"key": key, "isbns": isbn})
        except Exception:
            goodreads_status = False
        else:
            goodreads_status = True
        finally:
            return res.json() if goodreads_status and res.status_code == 200 else False

