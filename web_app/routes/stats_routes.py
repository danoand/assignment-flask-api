from sklearn.datasets       import load_iris
from sklearn.linear_model   import LogisticRegression

from flask import (Blueprint,
    jsonify,
    request,
    flash,
    redirect,
    render_template
    )

from web_app.models                     import User
from web_app.pred_model                 import load_model
from web_app.services.basilica_service  import connection as basilica_conn

# Define a stats routes blueprint
stats_routes = Blueprint("stats_routes", __name__)

# Route '/stats/iris' generates a prediction
@stats_routes.route("/stats/iris")
def iris():
    # Get iris data
    X, y = load_iris(return_X_y=True)
    # Load the persisted model from disk
    clf  = load_model()
    result = str(clf.predict(X[:2, :]))

    return render_template(
        "pred_iris.html", 
        result=result)

# Route '/stats/predict' makes a prediction between two twitter accounts
@stats_routes.route("/stats/predict", methods=["POST"])
def twitoff_predict():
    print(f"INFO: begin predict route processing")
    # Grab form data
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text    = request.form["tweet_text"]
    print(f"INFO: name1: {screen_name_a} name2: {screen_name_b} tweet: {tweet_text}")

    # Grab tweet embeddings associated with the entered data
    tweet_embeddings = []
    tweet_labels     = []
    # Fetch the objects for user a and user b from the database
    user_a = User.query.filter(User.screen_name == screen_name_a).one()
    user_b = User.query.filter(User.screen_name == screen_name_b).one()

    tweets_a   = user_a.tweets 
    tweets_b   = user_b.tweets
    all_tweets = tweets_a + tweets_b

    # Iterate through tweets
    for tweet in all_tweets:
        tweet_embeddings.append(tweet.embedding)
        tweet_labels.append(tweet.user.screen_name)

    print("EMBEDDINGS:", len(tweet_embeddings), "LABELS:", len(tweet_labels))

    # Define and fit a model
    print(f"INFO: generating a Logistic Regression model")
    classifier = LogisticRegression(
        random_state=0,
        solver="lbfgs",
        multi_class="multinomial"
    )
    print(f"INFO: fitting the Logistic Regression model")
    print(f"INFO: type tweet_embeddings: {type(tweet_embeddings)}")
    print(f"INFO: shape tweet_labels: {type(tweet_labels)}")
    classifier.fit(tweet_embeddings, tweet_labels)

    # Generate a prediction
    example_tweet_embedding = basilica_conn.embed_sentence(tweet_text, model="twitter")
    print(f"INFO: just before the prediction step")
    result = classifier.predict([example_tweet_embedding])
    print(f"INFO: just after the prediction step")

    return render_template("prediction_results.html",
        screen_name_a=screen_name_a,
        screen_name_b=screen_name_b,
        tweet_text=tweet_text,
        screen_name_most_likely=result[0])




