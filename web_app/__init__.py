from flask import Flask

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.tweet_routes import tweet_routes

DATABASE_URI = "sqlite://///Users/danoand/Documents/Companies/LambdaSchool/Assignments/DS-Unit-3-Sprint-3-Productization-and-Cloud/assignment/twitoff-dev.db"
SECRET_KEY = "my_secret_key_123"

def create_app():
    app = Flask(__name__)

    # Set a secret key to encrypt client side data 
    app.config["SECRET_KEY"] = SECRET_KEY

    # Configure database information
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database and database migration objects
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprint routes
    app.register_blueprint(home_routes)
    app.register_blueprint(tweet_routes)
    
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
