import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
# MongoDB stores data in a JSON-like format called bson.
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

# Once Flask is imported,create an instance of this and store in app variable
# the argument of Flask class is the name of the applications module __name__
# which is a built-in Python variable. Flask needs it to knows where to look
# for templates and static files.
app = Flask(__name__)
# first configuration will be used to grab the db name
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
# to configure the actual connection string
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# SECRET_KEY required when using some functions from Flask
app.secret_key = os.environ.get("SECRET_KEY")

# To ensure Flask app is communicating with Mongo db
mongo = PyMongo(app)

# @route decorator to wrap function and trigger it when browsing the directory
# Flask expects to be a directory called templates,on the same level as run.py
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username already exist in db and store that in a variable
        # set it to look for a user with find_one() method in users collection
        existing_user = mongo.db.users.find_one(
            # Look for the key username in db,the value will be the form data
            # username input(Python looks name="" attribute from html form)
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists, please choose a different one")
            # redirect the user back to the url_for()'register' function
            # to try again with another username.
            return redirect(url_for("register"))

        # if no existing user,take data from form into the register dictionary
        register = {
            "username": request.form.get("username").lower(),
            "email": request.frm.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
            }
        # call the users collection on MongoDB and use insert_one() method
        mongo.db.users.insert_one(register)

        # puts new user into a session temp cookie,imported from flask
        session["user"] = request.form.get("username").lower()
        flash("Registration Completed")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hased pass matches user input,check_pass_hash comes from
            # Werkzeug helper,takes 2 arguments: the existing_user hashed pass
            # on the db in [] and the pass from the form input.
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                # now log the user in using session variables called user
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(request.form.get("username")))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # it defaults "GET" method, which acts as the 'else' condition.
            flash("Username does not exist")
            return redirect(url_for("login.html"))

    return render_template("login.html")


@app.route("/characters")
def characters():
    characters = mongo.db.woman_card.find()

    return render_template("characters.html", characters=characters)


@app.route("/statistics")
def statistics():
    return render_template("statistics.html")


# __main__ is the name of the default module in Python.
if __name__ == "__main__":
    # Internal environment variable that gitpod has set,using the os module
    # from the standard library to get that environment variable.
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # during testing only
            debug=True)
