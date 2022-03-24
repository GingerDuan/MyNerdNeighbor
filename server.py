"""The server for app My Nerdy Nerighbor"""

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

API_KEY = os.environ['GoogleBook_Key']
# API_KEY = 'AIzaSyCNg1gcOesPKmO73lc_9lHZoSS2IyKwI4U'

@app.route("/")
def homepage():
    """View homepage"""
    
    return render_template("homepage.html")

@app.route("/user_profile/<user_id>")
def show_user_ownpage(user_id):
    """View users ownpage"""
    
    user = crud.get_user_by_id(user_id)
    
    return render_template("user_profile.html",user=user)

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
        new_user_id = user.user_id

        db.session.add(user)
        db.session.commit()
        flash("Account was created successfully!")
        return redirect(f"/user_profile/{new_user_id}")

    

@app.route("/login", methods=["POST"])
def login():
    """User login"""
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user.password == password: 
        
        
        session['user_email'] = user.email
        flash(f"Welcome back, {user.name}!")
        return redirect(f'/user_profile/{user.user_id}')

    else: 
        flash("Sorry, passwords or email do not match!")
        return redirect("/")

@app.route("/Boogle/")
def book_finder():
    """Search for book in Google book"""
    
    return render_template('Boogle.html')

@app.route("/Boogle/<user_id>")
def book_searcher(user_id):
    """Search for book in Google book"""
    user = crud.get_user_by_id(user_id)

    return render_template('Boogle.html',user=user)

@app.route("/search")
def book_search():
    """Send the payload to javascript"""

    keyword = request.args.get('keyword', '')
    url = 'https://www.googleapis.com/books/v1/volumes'
    payload = {'q':keyword,'apikey': API_KEY}
    
    res = requests.get(url,params = payload)

    return jsonify(res.json())

@app.route("/push_into_shelf",methods=["POST"])
def book_adder(user_id):
    """Put the book in the default shelf"""

    book_id = request.json.get("book.id")
    title =request.json.get("book.volumeInfo.title")
    pic = request.json.get("book.volumeInfo.imageLinks.thumbnail")
    bookshelf_id = crud.get_bookshelf_by_userid(user_id).bookshelf_id
    
    book = crud.create_book(title,book_id,pic,bookshelf_id)





if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)






