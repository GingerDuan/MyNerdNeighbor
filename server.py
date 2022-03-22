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

API_KEY = os.environ["GoogleBook_Key"]


@app.route("/")
def homepage():
    """View homepage"""
    return render_template("homepage.html")

@app.route("/user_profile")
def show_all_users():
    """View all users"""
    user = "ginger"
    # users = crud.get_all_user()
    
    return render_template("user_profile.html")

@app.route("/users/<user_id>")
def user_profile(user_id):
    """View user's profiles"""

    # user = crud.get_user_by_id(user_id)

    return render_template("user_profile.html")

@app.route("/login", methods=["POST"])
def login():
    """User login"""
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user.password == password: 
        session['user'] = user.email
        flash(f"Welcome back, {user.email}!")
    else: 
        flash("Sorry, passwords do not match!")

    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    """Check if email exist. If not will allow user to register their email."""
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    
    if user is None:
        new_user = crud.create_user(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash("The account was created successfully!")
    else: 
        flash("You can't create an account with the same email, please try again!") 
    
    return redirect("/")

@app.route("/Boogle")
def view_all_movies():
    """Search for book in Google book"""

    return render_template('Boogle.html')
                        #    results=res_num)

@app.route("/search")
def book_search():
    """Send the payload to javascript"""

    keyword = request.args.get('keyword', '')
    url = 'https://www.googleapis.com/books/v1/volumes'
    payload = {'q':keyword,'apikey': API_KEY}
    
    res = requests.get(url,params = payload)

    return jsonify(res.json())




if __name__ == "__main__":
    # DebugToolbarExtension(app)
    # connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)






