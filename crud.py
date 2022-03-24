"""CRUD operations for mnn."""

from model import db, User, Book, Bookshelf, connect_to_db

#user
def create_user(email, name, password,zipcode):
    """Create and return a new user."""

    user = User(email=email, name=name, password=password,zipcode=zipcode)

    return user

def get_users():
    """Return all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return user email if it exists, else returns None """

    return User.query.filter(User.email == email).first()

#bookshelf
def create_bookshelf(user_id,book_id):
    """Create and return a bookshelf"""

    bookshelf = Bookshelf(user_id=user_id,book_id=book_id)

    return bookshelf
# def get_book_by_zipcode(zipcode):
#     """Return all the book in the same zipcode"""

#     return Book.query.get(zipcode)
def get_bookshelf_by_userid(user_id):
    """Return a bookshelf by userid"""

    return Bookshelf.query.get(user_id)
    
#book
def create_book(book_id,title, pic,book_shelf):
    """Create and return a new book with zipcode."""

    book= Book(book_id = book_id,title=title, pic=pic,book_shelf=book_shelf)

    return book

# def create_list(score, movie, user):
#     """Create and return a rating"""

#     rating = Rating(score=score, movie = movie, user=user)

#     return rating




if __name__ == '__main__':
    from server import app
    connect_to_db(app)