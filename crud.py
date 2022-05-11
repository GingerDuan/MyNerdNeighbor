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
def create_bookshelf(user_id):
    """Create and return a bookshelf"""

    bookshelf = Bookshelf(user_id=user_id)

    return bookshelf

# def get_book_by_zipcode(zipcode):
#     """Return all the book in the same zipcode"""

#     return Book.query.get(zipcode)

def get_bookshelf_by_userid(user_id):
    """Return a bookshelf by userid"""

    return Bookshelf.query.filter(Bookshelf.user_id == user_id).first()
    
#book
def create_book(bookshelf_id,user_id):
    """Create and return a new book."""
    
    
    newbook= Book(bookshelf_id = bookshelf_id ) #？
    
    db.session.add(newbook)
    db.session.commit()
    return newbook

#booklist
def get_shelf_by_userid(user_id):
    """get all the book that user saved => bookshelf!!"""
    # booklist = []
    shelves = Shelf.query.filter(Shelf.user_id == user_id).all()
    # for line in saved_booklist_talbe:
    #     booklist.append(line[0])

    return shelves





if __name__ == '__main__':
    from server import app
    connect_to_db(app)