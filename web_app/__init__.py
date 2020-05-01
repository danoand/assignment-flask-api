import os
from flask import Flask

from web_app.models import db, migrate
from web_app.routes.home_routes     import home_routes
from web_app.routes.tweet_routes    import tweet_routes
from web_app.routes.twitter_routes  import twitter_routes
from web_app.routes.admin_routes    import admin_routes
from web_app.routes.stats_routes    import stats_routes

DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('APP_SECRET_KEY')

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
    app.register_blueprint(twitter_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(stats_routes)
    
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
