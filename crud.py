"""CRUD operations for mnn."""

from model import db, User, Book, Shelf,Puting, connect_to_db
#user
def create_user(email, name, password,zipcode):
    """Create and return a new user."""

    user = User(email=email, name=name, password=password,zipcode=zipcode)
    #creat four default shelf when user create account
    user.shelves.append(Shelf(name='bookshelf'))
    user.shelves.append(Shelf(name='toread'))
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


def get_shelf_by_userid(user_id):
    """Return a bookshelf by userid"""

    return Shelf.query.filter(Shelf.user_id == user_id).all()
    
#book
def create_book(googlebook_id,title,author,cover):
    """Create and return a new book."""

    book= Book(googlebook_id = googlebook_id,title=title,author=author,cover=cover)
    
    return book

def get_book_by_googleid(googlebook_id):

    book = Book.query.filter_by(googlebook_id = googlebook_id).first()

    return book

def get_book_by_bookid(book_id):

    book = Book.query.filter_by(book_id = book_id).first()

    return book


#puting
def create_puting(shelf_id,book_id,user_id,note):
    """get a the book saved in shelf!!"""


    puting = Puting(shelf_id = shelf_id,book_id = book_id,user_id = user_id,note=note)

    return puting

def get_puting_by_shelfid(shelf_id):

    putings = Puting.query.filter_by(shelf_id = shelf_id).order_by(Puting.time.desc())
    
    return putings

def get_puting_by_putingid(puting_id):

    putings = Puting.query.filter_by(puting_id = puting_id).first()

    return putings

def get_puting_by_shelfid_boookid(shelf_id,book_id):

    puting = Puting.query.filter(Puting.shelf_id == shelf_id, Puting.book_id == book_id).first()

    return puting

def get_puting_by_book_no_user(book_id,user_id):

    putings = Puting.query.filter(Puting.book_id == book_id,Puting.user_id != user_id).all()

    return putings

def get_puting_by_book_userid(book_id,user_id):
    putings = Puting.query.filter(Puting.book_id == book_id, Puting.user_id == user_id).all()

    return putings
# def get_book_by_putingid(puting_id):

#     puting = get_puting_by_putingid(puting_id)
#     books = Book.query.filter_by(book_id = puting.book_id).all()
    
#     return books


#get zipuser
def get_users_in_zipcode(user_id):

    user = User.query.get(user_id)
    zipusers = User.query.filter_by(zipcode = user.zipcode).all()

    return zipusers

def get_users_amount_in_zipcode(user_id):
    
    user = User.query.get(user_id)
    neighbor_num = User.query.filter_by(zipcode = user.zipcode).count()

    return neighbor_num

def get_books_in_zipcode(user_id):

    bookshelf_ids = []
    zipusers = get_users_in_zipcode(user_id)

    for user in zipusers:
        bookshelf_ids.append((user.user_id * 4)-3)

    books = []
    for bookshelf_id in bookshelf_ids:
        putings = Puting.query.filter_by(shelf_id=bookshelf_id).all()
        for puting in putings:
            books.append(puting.book)
    
    return books

def get_puting_in_zipcode(user_id):

    bookshelf_ids = []
    zipusers = get_users_in_zipcode(user_id)
    for user in zipusers:
        shelves = get_shelf_by_userid(user.user_id)
        for shelf in shelves:
            bookshelf_ids.append(shelf.shelf_id)
    putings = []
    # for bookshelf_id in bookshelf_ids:
        # puting_in_shelf = Puting.query.filter_by(shelf_id=bookshelf_id).order_by(Puting.time.desc())
    putings = Puting.query.filter(Puting.shelf_id.in_(bookshelf_ids)).order_by(Puting.time.desc())
        
    
        
           
    return putings


if __name__ == '__main__':
    from server import app
    connect_to_db(app)