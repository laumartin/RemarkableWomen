import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
# MongoDB stores data in a JSON-like format called bson.
# ObjectId from BSON,allows render MongoDB docs by their ID.
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


@app.route("/characters")
def characters():
    characters = mongo.db.woman_card.find()
    return render_template("characters.html", characters=characters)


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
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
            }
        # call the users collection on MongoDB and use insert_one() method
        mongo.db.users.insert_one(register)

        # puts new user into a session temp cookie,imported from flask
        session["user"] = request.form.get("username").lower()
        flash("Registration Completed")
        return redirect(url_for("profile", username=session["user"]))

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
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # it defaults "GET" method, which acts as the 'else' condition.
            flash("Username does not exist")
            return redirect(url_for("login.html"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # creates new username var, that is the user from db on the registered
    # users collection. The session variable in [] called 'user' for
    # consistency, and we only grab the username key field from the db record
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    # to avoid user's force the URL to someone else's profile create condition
    # so that only if the user session cookie is true, then return the profile.
    if session["user"]:
        # 1st username is what the template expects to retrieve in html file
        # the second username is the variable defined above
        return render_template("profile.html", username=username)
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have logged out from your account")
    # remove user from user session cookies and redirect to login page
    session.pop("user")
    return redirect(url_for("login"))


@app.route('/add_character', methods=["GET", "POST"])
def add_character():
    #this function allows the user to add a character to db
    if request.method == "POST":
        character = {
            # this use the name attributes from the character form to grab data
            # and that's what gets stored into mongo db in a dictionary
            "category_name": request.form.get("category_name"),
            "woman_name": request.form.get("woman_name"),
            "year": request.form.get("year"),
            "country_name": request.form.get("country_name"),
            "quote": request.form.get("quote"),
            "story": request.form.get("story"),
            "image": request.form.get("image"),
            "area_name": request.form.getlist("area_name"),
            "more_link": request.form.get("more_link"),
            "username": session["user"]
            }
        # use character variable into woman_card collection
        mongo.db.woman_card.insert_one(character)
        flash("Character Successfully included")
        return redirect(url_for("characters"))
    # perform find() method on categories collection sorted by name
    categories = mongo.db.categories.find().sort("category_name", 1)
    # perform find() method on countries collection sorted by name
    countries = mongo.db.countries.find().sort("country_name", 1)
    # display list of skills options from mongo db for checkbox character form
    area = list(mongo.db.skilled_area.find({}, {"area_name"}))

    return render_template(
        "add_character.html", categories=categories, countries=countries,
        skilled_area=area)


@app.route("/edit_character/<character_id>", methods=["GET","POST"])
# This function retrieve a character from the db that we want to edit by its ID
def edit_character(character_id):
    if request.method == "POST":
        submit_edit = {
            # this use the name attributes from the character form to grab data
            # and that's what gets stored into mongo db in a dictionary
            "category_name": request.form.get("category_name"),
            "woman_name": request.form.get("woman_name"),
            "year": request.form.get("year"),
            "country_name": request.form.get("country_name"),
            "quote": request.form.get("quote"),
            "story": request.form.get("story"),
            "image": request.form.get("image"),
            "area_name": request.form.getlist("area_name"),
            "more_link": request.form.get("more_link"),
            "username": session["user"]
            }
        # 1st argument is the character to update targeted by id and
        # 2nd is the submit_edit variable which contains all form elements
        mongo.db.woman_card.update(
            {"_id": ObjectId(character_id)}, submit_edit)
        flash("Character Updated")

    # The variable character uses find_one method on woman_card collection
    # and look for the key of _id
    character = mongo.db.woman_card.find_one({"_id": ObjectId(character_id)})

    categories = mongo.db.categories.find().sort("category_name", 1)
    # display list of skills options from mongo db for checkbox character form
    countries = mongo.db.countries.find().sort("country_name", 1)
    area = list(mongo.db.skilled_area.find({}, {"area_name"}))

    return render_template(
        "edit_character.html", character=character, categories=categories,
        countries=countries, skilled_area=area)


@app.route("/delete_character/<character_id>")
# for user to be able to delete a character he has added
def delete_character(character_id):
    mongo.db.woman_card.remove({"_id": ObjectId(character_id)})
    flash("Character Removed")
    return redirect(url_for("characters"))


@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("admin_manage.html", categories=categories)


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
