from flask import (Blueprint, 
    jsonify, 
    render_template, 
    request, 
    flash, 
    redirect, 
    url_for)

from web_app.models import db, Tweet, parse_rows

tweet_routes = Blueprint("tweet_routes", __name__)

@tweet_routes.route("/tweets.json")
def list_tweets():
    tweet_records = Tweet.query.all()
    print(tweet_records)
    tweets_response = parse_rows(tweet_records)
    return jsonify(tweets_response)

@tweet_routes.route("/")
def index_route():
    return redirect("/tweets")

@tweet_routes.route("/tweets")
def list_tweets_for_humans():
    tweet_records = Tweet.query.all()
    print(f"INFO: display {len(tweet_records)} tweets to the user")
    return render_template("tweets.html", message="Here are some tweets!", tweets=tweet_records)

@tweet_routes.route("/tweets/new")
def new_tweet():
    return render_template("new_tweet.html")

@tweet_routes.route("/tweets/create", methods=["POST"])
def create_tweet():
    print("FORM DATA:", dict(request.form))

    # Create a new Tweet model object
    new_tweet = Tweet(full_text=request.form["tweet_tweet"], user_id=request.form["tweet_handle"])
    # Add and commit to the database
    db.session.add(new_tweet)
    db.session.commit()

    # Display a flash meessage
    flash(f"Tweet '{new_tweet.full_text}' created successfully!", "success")
    return redirect("/tweets")
