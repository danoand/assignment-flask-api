import os

from flask import (Blueprint,
    jsonify,
    request,
    render_template,
    flash,
    redirect)

# API Key
API_KEY = os.environ.get('FL_APP_SECRET_KEY')

# Import the db object for use in this module
from web_app.models import db

# Define a Blueprint instance with this module name
admin_routes = Blueprint("admin_routes", __name__)

# Define a reset route
@admin_routes.route("/admin/db/reset")
def reset_db():
    # Grab arguments from the URI
    if len(request.args) == 0:
        print(f"ERROR: query arguments missing")
        flash("Missing API Key. Please check and try again", "danger")
        return redirect("/db_reset")

    if "api_key" not in dict(request.args):
        print(f"ERROR: missing API Key. Reset database not allowed")
        flash("Missing API Key. Please check and try again", "danger")
        return redirect("/db_reset")

    if request.args["api_key"] != API_KEY:
        print(f"WARN: invalid API Key. Reset database not allowed")
        flash("Invalid API Key. Please check and try again", "danger")
        return redirect("/db_reset")

    print(f"INFO: resetting the database")
    db.drop_all()   # drop all tables
    db.create_all() # create tables from scratch
    print(f"INFO: database has been reset")
    flash('Your database has been reset!', "success")
    return redirect("/db_reset")
