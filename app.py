import os
from flask import Flask, render_template

# Once Flask is imported,create an instance of this and store in app variable
# the argument of Flask class is the name of the applications module __name__
# which is a built-in Python variable. Flask needs it to knows where to look
# for templates and static files.
app = Flask(__name__)

# @route decorator to wrap function and trigger it when browsing the directory
# Flask expects to be a directory called templates,on the same level as run.py
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/characters")
def characters():
    return render_template("characters.html")


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
