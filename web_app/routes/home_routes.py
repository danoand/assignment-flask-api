from flask import Blueprint

home_routes = Blueprint("home_routes", __name__)

# Define the about route
@home_routes.route("/about")
def about():
    print("YOU VISITED THE ABOUT PAGE")
    return "About Me"
