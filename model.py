"""Models for My Nerd Neighbor app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    # ratings = a list of Rating objects

    def __repr__(self):
        return f'<User id user_id={self.user_id} Name name = {self.name} email={self.email}>'

class BookShelf(db.Model):
    """A Bookshlef pysically exits"""
    __tablename__ = "bookshelves"

    bookshelf_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    zipcode = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey("User.user_id"))

    def __repr__(self):
        return f'<User id user_id={self.user_id} Name name = {self.name} email={self.email}>'

class Book(db.Model):
    """A Book get from Google api"""
    
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True)#from Google Book
    bookshelf_id = db.Column(db.Integer,db.ForeignKey("BookShelf.bookshelf_id"))
    ISBN_code = db.Column(db.String,unique=True)#from Google Book
    status = db.Column(db.boolean)

    def __repr__(self):
        return f'<Book book_id={self.book_id} title={book.title}>'


def connect_to_db(flask_app, db_uri="postgresql:///user_profile", echo=True):
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
