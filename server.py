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

@app.route("/")
def homepage():
    """View homepage"""
    # if "user_id" in session:
        
    #     return redirect(f'/user_profile/{session["user_id"]}')
    
    return render_template("homepage.html")

@app.route("/user_profile/")
def show_user_ownpage():
    """View users ownpage"""
    
    if "user_id" not in session:
        return redirect('/')
    else:     
        user = crud.get_user_by_id(session["user_id"])
        booklist = crud.get_users_saved_booklist(session["user_id"])
        return render_template("user_profile.html",user=user,booklist=booklist)
        
    

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
        bookshelf = crud.create_bookshelf(user.user_id)
        
        db.session.add(bookshelf)
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
    if user.password == password: 
        
        
        session['user_id'] = user.user_id
        
        flash(f"Welcome back, {user.name}!")
        return redirect(f'/user_profile/')

    else: 
        flash("Sorry, passwords or email do not match!")
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

@app.route("/search")
def book_search():
    """Send the payload to javascript"""

    keyword = request.args.get('keyword', '')
    url = 'https://www.googleapis.com/books/v1/volumes'
    payload = {'q':keyword,'apikey': API_KEY}
    
    res = requests.get(url,params = payload)

    return jsonify(res.json())

@app.route("/push_into_shelf",methods=["POST"])
def book_adder():
    """Put the book in the default shelf"""

    book_id = request.json.get("book_id")
    user_id = session["user_id"]
    
    crud.create_book_inshelf(book_id,user_id)


    return {"success": True, "status": "You've added this book to your bookshelf!"}





if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)






