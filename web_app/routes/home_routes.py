from flask import (Blueprint, 
    render_template,
    redirect)

home_routes = Blueprint("home_routes", __name__)

# Define the /home route
@home_routes.route("/home")
def home():
    print("INFO: user visiting the /home route")
    return redirect("/tweets")

# Define the /about route
@home_routes.route("/about")
def about():
    print("INFO: user visiting the /home route")
    return redirect("/tweets")

# Define a general info route (to display to the user)
@home_routes.route("/db_reset")
def db_reset():
    return render_template("db_reset.html")

# Define a general info route (to display database updates to the user)
@home_routes.route("/call_twitter")
def call_twitter_reset():
    return render_template("call_twitter.html")

