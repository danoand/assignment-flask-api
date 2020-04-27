from flask import Blueprint, jsonify

from web_app.models                     import db, User, Tweet, parse_rows
from web_app.services.twitter_service   import api as twitter_api
from web_app.services.basilica_service  import connection as basilica_connection

twitter_routes = Blueprint("twitter_routes", __name__)

# Define a twitter route
@twitter_routes.route("/users/<screen_name>/fetch")
def fetch_user_data(screen_name):
    print("FETCHING...", screen_name)

    # Fetch user info from the Twitter API
    user = twitter_api.get_user(screen_name)

    # store user info in the database
    db_user = User.query.get(user.id) or User(id=user.id)
    db_user.screen_name     = user.screen_name
    db_user.name            = user.name
    db_user.location        = user.location
    db_user.followers_count = user.followers_count
    db.session.add(db_user)
    db.session.commit()

    # fetch the user's tweets
    statuses = twitter_api.user_timeline(
        screen_name, 
        tweet_mode="extended", 
        count=50)
    print("STATUSES", len(statuses))

    # fetch embedding for each tweet
    tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_connection.embed_sentences(
        tweet_texts,
        model="twitter"))

    print("EMBEDDINGS", len(embeddings))

    # store tweets and associated embeddings in the database
    for idx, status in enumerate(statuses):
        print(status.full_text)
        print("----")

        db_tweet            = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id    = status.author.id 
        db_tweet.full_text  = status.full_text 
        embedding           = embeddings[idx]

        print(len(embeddings))

        db_tweet.embed_sentences = embedding
        db.session.add(db_tweet)

    db.session.commit()

    return f"FETCHED {screen_name} OK"

