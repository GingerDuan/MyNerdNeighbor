"""The server for app My Nerdy Nerighbor"""

from multiprocessing import AuthenticationError
# from turtle import title
from flask import (Flask, render_template, request, flash, session,jsonify,
                   redirect)
from model import connect_to_db, db           
from jinja2 import StrictUndefined
import crud
import os
import requests

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# API_KEY = os.environ['GoogleBook_Key']

@app.route("/")
def homepage():
    """View homepage"""
    # if "user_id" in session:
        
    #     return redirect(f'/user_profile/{session["user_id"]}')
    flash (session)
    if "user_id" in session:
        user = crud.get_user_by_id(session["user_id"])
        flash(f'Hi! {user.name} You are log in')
        
        return render_template("homepage.html",user = user)
        
    else:
        flash("You need log in XD")
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
        
        
        
        books = []
        for shelf in bookshelves:

            putings = crud.get_puting_by_shelfid(shelf.shelf_id)

            for puting in putings:
                
                book_id = puting.book_id
                book = crud.get_book_by_bookid(book_id)
                books.append(book)

            # if s == 1:
            #     bookshelf = crud.get_puting_by_shelfid(shelf.shelf_id)
            # if s == 2:
            #     to_read = crud.get_puting_by_shelfid(shelf.shelf_id)
            # if s == 3:
            #     reading = crud.get_puting_by_shelfid(shelf.shelf_id)
            # if s == 4:
            #     have_read = crud.get_puting_by_shelfid(shelf.shelf_id)
            
            # s += 1
        
        return render_template("user_profile.html",user=user,bookshelves=bookshelves,books = books)
        
    

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

@app.route("/Boogle")
def book_finder():
    """Search for book in Google book"""
    if "user_id" in session:
        user = crud.get_user_by_id(session["user_id"])
    else:
        user = None
    return render_template('Boogle.html',user=user)

# @app.route("/Boogle/<user_id>")
# def book_searcher(user_id):
#     """Search for book in Google book"""
#     user = crud.get_user_by_id(user_id)

#     return render_template('Boogle.html',user=user)

@app.route("/boogle2")
def show_boogle():
    return render_template('boogle2.html')

@app.route("/search")
def book_search():
    """Send the payload to javascript"""

    keyword = request.args.get('keyword', '')
    title = request.args.get("title",'')
    author = request.args.get('author','')
    year = request.args.get("year",'')

    url = 'https://www.googleapis.com/books/v1/volumes'
    payload = {'q':keyword,
                'title' : title,
                'author' : author,
                'year' : year,
                'startIndex':0,
                'maxResults':5,}
    
    res = requests.get(url,params = payload)
    data = res.json()

    return render_template('boogle_res.html', data = data,keyword=keyword)


@app.route("/put_into_shelf",methods=["POST"])
def book_adder():
    """Put the book in the user's shelf"""

    googlebook_id = request.json.get("googlebook_id")
    user_id = session["user_id"]
    anybook = crud.get_book_by_googleid(googlebook_id)
    shelf_id = 4 * (user_id-1) + 1


    if anybook:
        
        puting = crud.create_puting(shelf_id = shelf_id,book_id = anybook.book_id)
        
        db.session.add(puting)
        db.session.commit()
        return anybook.book_id
    else: 
        url = f'https://www.googleapis.com/books/v1/volumes/{googlebook_id}'
        
        response = requests.get(url)
        data = response.json()
        
        title = data['volumeInfo']['title']
        author = data['volumeInfo']['authors'][0]
        cover = data['volumeInfo']['imageLinks']['thumbnail']
        
        #cover = request.json.get("cover","https://icon-library.com/images/book-icon-png/book-icon-png-28.jpg")
        newbook = crud.create_book(googlebook_id,title,author,cover)
        db.session.add(newbook)
        db.session.commit()
        puting = crud.create_puting(shelf_id = shelf_id,book_id = newbook.book_id)

        db.session.add(puting)
        db.session.commit()
        return jsonify({"status":googlebook_id })
   

        
        




if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)






