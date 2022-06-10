"""The server for app My Nerdy Nerighbor"""

from multiprocessing import AuthenticationError
# from turtle import title
from flask import (Flask, render_template, request, flash, session,jsonify,
                   redirect)
from model import connect_to_db, db           
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

    
    # if "user_id" in session:
    #     user = crud.get_user_by_id(session["user_id"])
    #     flash(f'Hi! {user.name} You are log in')
        
    #     return render_template("homepage.html",user = user)
        
    # else:
    #     flash("You need log in XD")
    return render_template("homepage.html")

@app.route("/user_profile/")
def show_user_ownpage():
    """View users ownpage"""
    
    if "user_id" not in session:
        flash("you did not log in")
        return redirect('/')
    else:
        user_id = session["user_id"]
        user = crud.get_user_by_id(user_id)

        bookshelves = crud.get_shelf_by_userid(user_id)

        own_putings = crud.get_puting_by_shelfid(bookshelves[0].shelf_id)
        toread_putings = crud.get_puting_by_shelfid(bookshelves[1].shelf_id)
        reading_putings = crud.get_puting_by_shelfid(bookshelves[2].shelf_id)
        haveread_putings = crud.get_puting_by_shelfid(bookshelves[3].shelf_id)
        
        return render_template("user_profile.html",user=user,bookshelves=bookshelves,own_putings=own_putings,toread_putings=toread_putings,reading_putings=reading_putings,haveread_putings=haveread_putings)
        
    

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
        return redirect("/")
    else:
        user = crud.create_user(email,name,password,zipcode)
        
        
        db.session.add(user)
        db.session.commit()

        new_user_id = user.user_id

        session['user_id'] = new_user_id

        flash("Account was created successfully!")
        return redirect(f"/user_profile/")

    

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
        return redirect("/")

@app.route("/logout")
def logout():
    """Log user out, delete session"""
    
    del session['user_id']

    return redirect('/')

# @app.route("/Boogle")
# def book_finder():
#     """Search for book in Google book"""
#     if "user_id" in session:
#         user = crud.get_user_by_id(session["user_id"])
#     else:
#         user = None
#     return render_template('Boogle.html',user=user)



@app.route("/boogle2")
def show_boogle():
    return render_template('boogle2.html')

@app.route("/search")
def book_search():
    """Send the request and get the api data"""

    keyword = request.args.get('keyword','')
    # intitle = request.args.get("title",'')
    # author = request.args.get('author','')
    # isbn = request.args.get("isbn",'')
    # inpublisher = request.args.get("publisher","")

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
        return redirect("/boogle2")

@app.route("/search_detail")
def search_detail():

    return render_template("boogle_detail.html")
    

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
            puting = crud.create_puting(shelf_id = shelf_id,book_id = anybook.book_id,user_id = user_id,note=note)
        
            db.session.add(puting)
            db.session.commit()
            return jsonify({"status":f'{anybook.title} add in your shelf' })
    else: 
        url = f'https://www.googleapis.com/books/v1/volumes/{g_id}'
        
        response = requests.get(url)
        data = response.json()
        
        title = data['volumeInfo']['title']
        author = data['volumeInfo']['authors'][0]
        if 'imageLinks' in data['volumeInfo']:
            cover = data['volumeInfo']['imageLinks']['thumbnail']
        else:
            cover = None
        
        newbook = crud.create_book(googlebook_id=g_id,title=title,author=author,cover=cover)
        db.session.add(newbook)
        db.session.commit()
        puting = crud.create_puting(shelf_id = shelf_id,book_id = newbook.book_id,user_id=user_id,note=note)

        db.session.add(puting)
        db.session.commit()
        return jsonify({"status":f'{newbook.title} add in your shelf' })


#neighborpage
@app.route("/neighborlibrary")
def show_ntighbor_books():

    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)
    zipusers = crud.get_users_in_zipcode(user_id)
    neighbor_num = crud.get_users_amount_in_zipcode(user_id)
    books = crud.get_books_in_zipcode(user_id)

    return render_template('neighbor_library.html',zipusers=zipusers,user=user,neighbor_num=neighbor_num,books= books)
        
@app.route("/neighbor")  
def show_neighbor_puting():

    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)
    zipusers = crud.get_users_in_zipcode(user_id)
    neighbor_num = crud.get_users_amount_in_zipcode(user_id)
    putings = crud.get_puting_in_zipcode(user_id)

    return render_template('neighbor.html',zipusers=zipusers,user=user,neighbor_num=neighbor_num,putings=putings)

#create a new book
@app.route("/upload")
def book_upload_page():

    return render_template('create_book.html')

@app.route("/pro_upload2", methods =['POST'])
def book_uploaderr():

    my_file = request.files["my_file"]    
    result = cloudinary.uploader.upload(my_file,
                                        api_key=CLOUDINARY_KEY,
                                        api_secret=CLOUDINARY_SECRET,
                                        cloud_name=CLOUD_NAME)
    img_url = result['secure_url']
    
    authors = []
    title = request.form.get("title")
    author = request.form.get("authors")
    if "+" in author:
        authors = author.split("+")
    else:
        authors.append(str(author))
    

    date = request.form.get("time")
    
    publisher = request.form.get("publisher")
    des = request.form.get("des")

    newbook = crud.create_a_new_book(title=title,author=authors,cover=img_url,date=date,publisher= publisher,description = des)
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

    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)

    if len(id) < 6:
        anybook = crud.get_book_by_bookid(id)
        book = None
        year = None
        data = None

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

    return render_template("bookpage.html",anybook = anybook, book=book,year=year,data=data,
    own_putings = own_putings,others_putings=others_putings,user=user)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)






