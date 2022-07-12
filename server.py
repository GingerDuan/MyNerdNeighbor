"""The server for app My Nerdy Nerighbor"""

from multiprocessing import AuthenticationError
# from turtle import title
from flask import (Flask, render_template, request, flash, session,jsonify,
                   redirect)
from model import Book, Puting, connect_to_db, db           
from jinja2 import StrictUndefined
from datetime import datetime
import crud
import cloudinary.uploader
import os
import requests

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME ="my-nerd-neighbor"
API_KEY = os.environ['googlebookapi_key']

@app.route("/")
def homepage():
    """View homepage"""

    
    if "user_id" in session:
        user = crud.get_user_by_id(session["user_id"])
        flash(f'Hi! {user.name} You are log in')
        
        return render_template("homepage.html",user = user)
        
    else:
        flash("Hi there, welcome to my nerd nrighbor!")
        return render_template("homepage.html")

@app.route("/user_profile/")
def show_user_ownpage():
    """View users ownpage"""
    
    if "user_id" not in session:
        flash("AHH,You did not log in!")
        return redirect('/')
    else:
        user_id = session["user_id"]
        user = crud.get_user_by_id(user_id)

        bookshelves = crud.get_shelf_by_userid(user_id)
        putings = crud.get_puting_by_user_id(user_id)
        
        return render_template("user_profile.html",user=user,bookshelves=bookshelves,putings=putings)

@app.route("/user_profile/<userid>")
def show_users_page(userid):
    """View users ownpage"""
    
    user = crud.get_user_by_id(userid)
    bookshelves = crud.get_shelf_by_userid(userid)
    putings = crud.get_puting_by_user_id(userid)  

    return render_template("user_profile.html",user=user,bookshelves=bookshelves,putings=putings)
        

@app.route("/user_shelves/")
def show_user_library():
    """View users ownpage"""
    
    if "user_id" not in session:
        flash("you did not log in")
        return redirect('/')
    else:
        user_id = session["user_id"]
        user = crud.get_user_by_id(user_id)

        bookshelves = crud.get_shelf_by_userid(user_id)
        
        return render_template("user_library.html",user=user,bookshelves=bookshelves)
        
@app.route("/register")
def sign_in_page():

    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    """Check if email exist. If not will allow user to register, create a new user."""
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    zipcode = request.form.get("zipcode")

    user = crud.get_user_by_email(email)
    
    if user:
        flash("You can't create an account with the same email, please try another one!")
        return redirect("/register")
    else:
        user = crud.create_user(email,name,password,zipcode)
        
        
        db.session.add(user)
        db.session.commit()

        new_user_id = user.user_id

        session['user_id'] = new_user_id

        flash("Account was created successfully!")
        return redirect(f"/user_profile/")

@app.route("/login_page")
def login_page():

    return render_template("login.html")    

@app.route("/login", methods=["POST"])
def login():
    """User login"""
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user == None:
        flash("Sorry, this email have not register yet!")
        return redirect("/")

    if user.password == password: 
               
        session['user_id'] = user.user_id
        
        flash(f"Welcome back, {user.name}!")
        return redirect(f'/user_profile/')

    else: 
        flash("Sorry, passwords do not match!")
        return redirect("/login_page")

@app.route("/logout")
def logout():
    """Log user out, delete session"""
    if 'user_id' in session:
        del session['user_id']
        
    else:
        
        flash("You are already log out!")
    return redirect('/')


@app.route("/boogle2")
def show_boogle():
    return render_template('boogle2.html')

@app.route("/search")
def book_search():
    """Send the request and get the api data"""

    keyword = request.args.get('keyword','')

    url = 'https://www.googleapis.com/books/v1/volumes?'
    payload = { "q":keyword,'maxResults':30,}
    
    res = requests.get(url,params=payload)
    data = res.json()

    if 'totalItems' in data:
        return render_template('boogle_res.html', payload=payload,data = data,keyword =keyword)
    else:
        flash("you need type something")
        return redirect("/boogle2")

@app.route("/search_author")
def author_search():
    """Send the request and get the api data"""
    
    
    author = request.args.get('author')

    if not author:
        flash("You need type in some author")
        return redirect("/boogle2")
    else:
        url = f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}&maxResults:30'
        res = requests.get(url)
        data = res.json()

        return render_template('boogle_res.html',data = data,keyword =author,url=url)
   

@app.route("/search_isbn")
def isbn_search():
    """Send the request and get the api data"""

    isbn = request.args.get("isbn",'')
    
    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&maxResults:30'
    
    
    res = requests.get(url)
    data = res.json()

    if 'totalItems' in data:
        return render_template('boogle_res.html',data = data,keyword=isbn)
    else:
        flash(f"you need type something {isbn}")
        return redirect("/boogle2")

@app.route("/search_publisher")
def publisher_search():
    """Send the request and get the api data"""

    keyword = request.args.get('keyword','')
    # intitle = request.args.get("title",'')
    # author = request.args.get('author','')
    # isbn = request.args.get("isbn",'')
    inpublisher = request.args.get("publisher","")

    url = 'https://www.googleapis.com/books/v1/volumes?'
    payload = { "q":keyword,
                # 'intitle' : intitle,
                # 'inauthor' : author,
                # "isbn" : isbn,
                # "inpublisher" : inpublisher,
                'maxResults':30,
                }
    
    res = requests.get(url,params=payload)
    data = res.json()

    if 'totalItems' in data:
        return render_template('boogle_res.html', payload=payload,data = data,keyword =keyword)
    else:
        flash("you need type something")
        return redirect("/boogle2")
    

@app.route("/remove_from_shelf",methods=["POST"])
def book_remover():
    """remove the book form the shelf"""

    puting_id = request.json.get("puting_id")
    
    find_puting = crud.get_puting_by_putingid(puting_id)

    db.session.delete(find_puting)
    db.session.commit()

    return jsonify({"status":"this book disappear" })


@app.route("/put_into_shelf",methods=["POST"])
def book_adder():
    """Put the book in the user's shelf"""
    user_id = session["user_id"]

    status_code = request.json.get("status")
    note = request.json.get("note")
    g_id = request.json.get("googlebook_id")
    if len(g_id) > 5:
        anybook = crud.get_book_by_googleid(g_id)
    else:
        anybook = crud.get_book_by_bookid(g_id)
    
    # covert shelf_name to a number to right shelf_id
    #status_code 0have read 1reading 2to read 3Iown this book
    shelf_id = (4 * user_id)- int(status_code)
    
    if anybook:
        anyputing = crud.get_puting_by_shelfid_boookid(shelf_id,anybook.book_id)
        if anyputing:
            return jsonify({"status":"this book has already in your shelf" })
        else:
            puting = crud.create_puting(shelf_id = shelf_id,book_id = anybook.book_id,user_id = user_id,note=note,time=datetime.now())
        
            db.session.add(puting)
            db.session.commit()
            return jsonify({"status":f'{anybook.title} add in your shelf' })
    else: 
        url = f'https://www.googleapis.com/books/v1/volumes/{g_id}'
        
        response = requests.get(url)
        data = response.json()
        
        title = data['volumeInfo']['title']
        if 'authors' in data['volumeInfo']:
            author = data['volumeInfo']['authors'][0]
        else:
            author = None

        if 'imageLinks' in data['volumeInfo']:
            cover = data['volumeInfo']['imageLinks']['thumbnail']
        else:
            cover = None
        
        newbook = crud.create_book(googlebook_id=g_id,title=title,author=author,cover=cover)
        db.session.add(newbook)
        db.session.commit()
        puting = crud.create_puting(shelf_id = shelf_id,book_id = newbook.book_id,user_id=user_id,note=note,time=datetime.now())

        db.session.add(puting)
        db.session.commit()
        return jsonify({"status":f'{newbook.title} add in your shelf' })


#neighborpage
@app.route("/neighbor_library")
def show_ntighbor_books():

    if "user_id" in session:

        user_id = session["user_id"]
        user = crud.get_user_by_id(user_id)
        zipusers = crud.get_users_in_zipcode(user_id)
        neighbor_num = crud.get_users_amount_in_zipcode(user_id)
        putings = crud.get_own_putings_in_zipcode(user_id)

        return render_template('neighbor_library.html',zipusers=zipusers,user=user,neighbor_num=neighbor_num,putings=putings)
    
    else:
        flash("You need login")
        return redirect("/")

@app.route("/neighbor_search",methods=["GET"])
def find_book_in_neighbor():

    user_id = session["user_id"]

    keyword = request.args.get("keyword")
    zipbooks = crud.get_books_in_zipcode(user_id)
    putings_res = [book.title for book in zipbooks if keyword in book.title]
    
    return jsonify({"putings":putings_res})

@app.route("/neighbor_feed")
def show_ntighbor():

    if "user_id" in session:
        user_id = session["user_id"]

        user = crud.get_user_by_id(user_id)
        zipusers = crud.get_users_in_zipcode(user_id)
        neighbor_num = crud.get_users_amount_in_zipcode(user_id)
        putings = crud.get_puting_in_zipcode(user_id)

        return render_template('neighbor.html',zipusers=zipusers,user=user,neighbor_num=neighbor_num,putings=putings)
    
    else:
        flash("You need login")
        return redirect("/")

#create a new book
@app.route("/upload")
def book_upload_page():

    return render_template('create_book.html')

@app.route("/pro_upload2", methods =['POST'])
def book_uploaderr():

    my_file = request.files["my_file"]
    if my_file == None:
        img_url = "https://cdn.pixabay.com/photo/2014/04/02/16/21/book-307045_960_720.png"    
    else:
        result = cloudinary.uploader.upload(my_file,
                                        api_key=CLOUDINARY_KEY,
                                        api_secret=CLOUDINARY_SECRET,
                                        cloud_name=CLOUD_NAME)
        img_url = result['secure_url']
    
    
    
    title = request.form.get("title")
    author = request.form.get("authors")

    date = request.form.get("time")
    
    publisher = request.form.get("publisher")
    des = request.form.get("des")

    newbook = crud.create_a_new_book(title=title,author=author,cover=img_url,date=date,publisher= publisher,description = des)
    db.session.add(newbook)

    db.session.commit()
    
    return redirect(f"/book/{newbook.book_id}")

@app.route("/pro_upload", methods =['POST'])
def book_uploader():

    my_file = request.files["my_file"]    
    result = cloudinary.uploader.upload(my_file,
                                        api_key=CLOUDINARY_KEY,
                                        api_secret=CLOUDINARY_SECRET,
                                        cloud_name=CLOUD_NAME)
    img_url = result['secure_url']
    
    gid = request.form.get("gid")
    book = crud.get_book_by_googleid(gid)
    
    if book != None:
        book.cover = img_url
    else:
        title = request.form.get("title")
        author = request.form.get("author")
        newbook = crud.create_book(googlebook_id=gid,title=title,author=author,cover=img_url)
        db.session.add(newbook)

    db.session.commit()

    return redirect(f"/book/{gid}")

#bookpage
@app.route("/book/<id>")
def show_book_detail(id):

    #when book user's create
    if len(id) < 6:
        anybook = crud.get_book_by_bookid(id)
        book = None
        year = None
        data = None

    #when book from googlebook
    else:
        anybook = crud.get_book_by_googleid(id)
        
        url = f'https://www.googleapis.com/books/v1/volumes/{id}'
        response = requests.get(url)
        data = response.json()
        book = data['volumeInfo']

        #year
        if 'publishedDate' in book:
            time = book["publishedDate"]
            if len(time) == 4:
                year = book["publishedDate"]
            elif len(time) < 8:
                year = year = datetime.strptime(time,"%Y-%m").year
            else:
                year = datetime.strptime(time,"%Y-%m-%d").year
        else:
            year = None

    #when user log in 
    if "user_id" in session:
   
        user_id = session["user_id"]
        user = crud.get_user_by_id(user_id)

        if anybook:

                if crud.get_puting_by_book_userid(anybook.book_id,user_id):
                    own_putings = crud.get_puting_by_book_userid(anybook.book_id,user_id)
                else:
                    own_putings = None

                if crud.get_puting_by_book_no_user(anybook.book_id,user_id):
                    others_putings = crud.get_puting_by_book_no_user(anybook.book_id,user_id)
                else:
                    others_putings = None

        else: 
            own_putings = None
            others_putings = None

    #when guest hanging out
    else:
        flash("You need login")
        own_putings = None
        others_putings = None
        user = None

    

    return render_template("bookpage.html",anybook = anybook, book=book,year=year,data=data,
    own_putings = own_putings,others_putings=others_putings,user=user)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)






