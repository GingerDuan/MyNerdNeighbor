"""CRUD operations for mnn."""

from model import db, User, Book, Shelf,Puting, connect_to_db

#user
def create_user(email, name, password,zipcode):
    """Create and return a new user."""

    user = User(email=email, name=name, password=password,zipcode=zipcode)
    #creat four default shelf when user create account
    user.shelves.append(Shelf(name='bookshelf'))
    user.shelves.append(Shelf(name='to read'))
    user.shelves.append(Shelf(name='reading'))
    user.shelves.append(Shelf(name='have read'))
    
    db.session.add(user)
    db.session.commit()

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
def create_shelf(user_id,name):
    """Create and return a bookshelf"""

    shelf = Shelf(user_id=user_id,name = name)

    return shelf

# def get_book_by_zipcode(zipcode):
#     """Return all the book in the same zipcode"""

#     return Book.query.get(zipcode)

def get_shelf_by_userid(user_id):
    """Return a bookshelf by userid"""

    return Shelf.query.filter(Shelf.user_id == user_id).all()
    
#book
def create_book(googlebook_id,title,author,cover):
    """Create and return a new book."""
    
    
    book= Book(googlebook_id = googlebook_id,title=title,author=author,cover=cover)
    
    db.session.add(book)
    db.session.commit()
    return book

#booklist
def create_puting(shelf_id,book_id,time,note):
    """get a the book saved in shelf!!"""
    
    puting = Puting(shelf_id = shelf_id,book_id = book_id,time = time,note = note)

    return puting





if __name__ == '__main__':
    from server import app
    connect_to_db(app)