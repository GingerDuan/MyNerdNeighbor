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

    shelves = db.relationship("Shelf", back_populates="user")

    def __repr__(self):
        return f'<user_id={self.user_id} name = {self.name} email={self.email}>'

class Shelf(db.Model):
    """A Booklist of I have/read/to read/reading/or anything"""
    __tablename__ = 'shelf'

    shelf_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"),nullable=False)
    name = db.Column(db.String)

    user = db.relationship("User", back_populates="shelves")
    

    def __repr__(self):
        return f'<shelf_name={self.name} Belong to user={self.user.name}>'

class Puting(db.Model):
    """middle table with book and shelf"""
    __tablename__ = "puting"

    puting_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    shelf_id = db.Column(db.Integer,db.ForeignKey("shelf.shelf_id"))
    book_id = db.Column(db.Integer,db.ForeignKey("books.book_id"))
    time = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    note = db.Column(db.Text,nullable=True)

    book = db.relationship("Book", backref="puting")
    shelf = db.relationship("Shelf", backref="puting") 

    def __repr__(self):
        return f'<pt={self.puting_id} shelf={self.shelf_id} book={self.book_id} time={self.time}>'

class Book(db.Model):
    """A Book's information first get from Google api"""
    
    __tablename__ = "books"

    book_id = db.Column(db.Integer,primary_key=True)
    googlebook_id = db.Column(db.String)
    title = db.Column(db.String(100))
    author = db.Column(db.String)
    cover = db.Column(db.String)   
    
    def __repr__(self):
        return f'<book_id={self.book_id} title={self.title} Googlebookid={self.googlebook_id}>'


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
