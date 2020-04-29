from flask import (Blueprint, 
    jsonify,
    flash,
    redirect)


from web_app.models                     import db, User, Tweet, parse_rows
from web_app.services.twitter_service   import api as twitter_api
from web_app.services.basilica_service  import connection as basilica_connection

twitter_routes = Blueprint("twitter_routes", __name__)

# Define a twitter route
@twitter_routes.route("/users/<screen_name>/fetch")
def fetch_user_data(screen_name):
    print("INFO: fetching twitter for inforation for: ", screen_name)

    # Fetch user info from the Twitter API
    user = twitter_api.get_user(screen_name)

    # Grab a user object from the database or create new
    db_user = User.query.get(user.id) or User(id=user.id)

    # Update user object data
    db_user.screen_name     = user.screen_name
    db_user.name            = user.name
    db_user.location        = user.location
    db_user.followers_count = user.followers_count

    # Update the database
    db.session.add(db_user)
    db.session.commit()
    print("INFO: update user information in the db for: ", screen_name)

    # Fetch the user's tweets
    statuses = twitter_api.user_timeline(
        screen_name, 
        tweet_mode="extended", 
        count=50)
    print("INFO: just recevied Twitter statuses number = ", len(statuses))

    # Fetch embeddings for each tweet
    tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_connection.embed_sentences(
        tweet_texts,
        model="twitter"))

    print("INFO: just received tweet embeddings number = ", len(embeddings))

    # store tweets and associated embeddings in the database
    ctr = 0
    for idx, status in enumerate(statuses):

        db_tweet            = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id    = status.author.id 
        db_tweet.full_text  = status.full_text 
        embedding           = embeddings[idx]

        db_tweet.embed_sentences = embedding
        db.session.add(db_tweet)
        ctr = ctr + 1

    print("INFO: storing and tweets and embeddings in the database number = ", ctr)
    db.session.commit()

    flash(f'Just stored tweet and embedding information into the database! Number of updates: {ctr}', "success")
    return redirect("/call_twitter")

