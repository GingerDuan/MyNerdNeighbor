"""Models for My Nerd Neighbor app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    zipcode = db.Column(db.String)
    password = db.Column(db.String)

    def __repr__(self):
        return f'<User id user_id={self.user_id} name = {self.name} email={self.email}>'

class Bookshelf(db.Model):
    """A Bookshlef pysically exits"""
    __tablename__ = "bookshelf"

    bookshelf_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"))
    # book_id = db.Column(db.Integer,db.ForeignKey("books.book_id")) don't need, one bookshelf t

    book = db.relationship("Book", backref="bookshelf")

    def __repr__(self):
        return f'<Bookshelf bookshelf_id={self.bookshelf_id} Belong to user={self.user_id}>'

class Book(db.Model):
    """A Book's information get from Google api"""
    
    __tablename__ = "books"

    book_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String)
    cover = db.Column(db.String)
    available = db.Column(db.Boolean, default= False)

    bookshelf_id = db.Column(db.Integer,db.ForeignKey("bookshelf.bookshelf_id"))

    # bookshelf = db.relationship("Bookshelf", backref = 'book')
    
    def __repr__(self):
        return f'<Book book_id={self.book_id} bookshelf={self.book}>'


def connect_to_db(flask_app, db_uri="postgresql:///bookapp", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
