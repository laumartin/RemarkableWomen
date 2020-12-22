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
    return render_template("register.html")


@app.route("/characters")
def characters():
    characters = mongo.db.woman_card.find()

    return render_template("characters.html", characters=characters)


@app.route("/login")
def login():
    return render_template("login.html")


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
