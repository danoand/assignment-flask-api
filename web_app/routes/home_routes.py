from flask import Blueprint, render_template

home_routes = Blueprint("home_routes", __name__)

# Define the about route
@home_routes.route("/about")
def about():
    print("YOU VISITED THE ABOUT PAGE")
    return "About Me"

# Define a general info route (to display to the user)
@home_routes.route("/db_reset")
def db_reset():
    return render_template("db_reset.html")

