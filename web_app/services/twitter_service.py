import tweepy
import os

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_API_TOKEN = os.getenv("TWITTER_API_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_API_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

if __name__ == "__main__":
    print("INFO: test fetching data from the Twitter API")

    user = api.get_user("@ycombinator")
    statuses = api.user_timeline("@ycombinator", tweet_mode="extended", count=35, exclude_replies=True, include_rts=False)
    status = statuses[0]

    print(f"INFO: first status for '@ycombinator': {status}")
    