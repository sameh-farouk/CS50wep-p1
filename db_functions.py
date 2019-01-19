from sqlalchemy import exc, text
import psycopg2
from db_helper import context_session


def talk_db(q):
    with context_session() as session:
        r = session.execute(q)
        return r


def register_this_user(name, emailAddress, password_hash):
    q = text('INSERT INTO users (name, emailAddress, password) VALUES (:name, :emailAddress, :password) RETURNING id, name').params(
        name=name, emailAddress=emailAddress, password=password_hash)
    with context_session() as session:
        try:
            r = session.execute(q)
        except exc.IntegrityError as e:
            print(e)
            return False
        return r.fetchone()


def get_user_by_email(emailAddress):
    q = text(
        'SELECT * FROM users WHERE emailAddress = :emailAddress').params(emailAddress=emailAddress)
    with context_session() as session:
        r = session.execute(q)

        if r.rowcount != 1:
            return False
        else:
            return r.first()


def update_user_last_seen(user_id):
    q = text('UPDATE users SET lastSeen = current_timestamp WHERE id = :user_id').params(
        user_id=user_id)
    with context_session() as session:
        r = session.execute(q)
        if r.rowcount != 1:
            return False
        else:
            return True


def search_for_books(searchword, page):
    per_page = 10
    i = (page - 1) * per_page
    q1 = text('SELECT * FROM books WHERE title ILIKE :searchword OFFSET :i LIMIT :per_page').params(
        searchword=f'%{searchword}%', i=i, per_page=per_page)
    q2 = text('SELECT * FROm books WHERE author ILIKE :searchword OFFSET :i LIMIT :per_page').params(
        searchword=f'%{searchword}%', i=i, per_page=per_page)
    q3 = text('SELECT * from books WHERE isbn ILIKE :searchword OFFSET :i LIMIT :per_page').params(
        searchword=f'%{searchword}%', i=i, per_page=per_page)
    with context_session() as session:
        r1 = session.execute(q1)
        r2 = session.execute(q2)
        r3 = session.execute(q3)
        match_title = r1.fetchall() if r1.rowcount else []
        match_author = r2.fetchall() if r2.rowcount else []
        match_isbn = r3.fetchall() if r3.rowcount else []
        return match_title, match_author, match_isbn


def get_book_by_isbn(isbn):
    q = text('SELECT * FROM books WHERE isbn = :isbn').params(isbn=str(isbn))
    with context_session() as session:
        r = session.execute(q)
        book = r.fetchone() if r.rowcount else False
        return book


def submit_this_review(rate, review, user_id, book_id):
    q = text('INSERT INTO reviews (book_id, user_id, rating, text) VALUES (:book_id, :user_id, :rating, :text) RETURNING id').params(
        book_id=book_id, user_id=user_id, rating=rate, text=review)

    with context_session() as session:
        try:
            r = session.execute(q)

        except exc.IntegrityError as e:
            print(e)
            return False
        else:
            return r.scalar()


def check_can_submit(book_id, user_id):
    q = text('SELECT id FROM reviews WHERE book_id = :book_id AND user_id = :user_id').params(
        book_id=book_id, user_id=user_id)
    with context_session() as session:
        r = session.execute(q)
        can_submit = False if r.rowcount else True
        return can_submit


def get_book_reviews(book_id):
    q = text('SELECT rating, text, added::timestamp(0), name FROM reviews JOIN users ON user_id = users.id WHERE book_id = :book_id ORDER BY added DESC').params(book_id=book_id)

    with context_session() as session:
        r = session.execute(q)

        reviews = r.fetchall() if r.rowcount else False
        return reviews


def get_user_reviews(user_id, page):
    per_page = 5
    i = (page - 1) * per_page

    q = text('SELECT rating, text, reviews.added::timestamp(0) as added, title, isbn FROM reviews JOIN books ON book_id = books.id WHERE user_id = :user_id ORDER BY reviews.added DESC OFFSET :i LIMIT :per_page').params(
        user_id=user_id, i=i, per_page=per_page)
    with context_session() as session:

        r = session.execute(q)
        user_reviews = r.fetchall() if r.rowcount else []
        return user_reviews
