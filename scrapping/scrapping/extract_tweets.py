import tweepy
from dotenv import load_dotenv
import os

load_dotenv()
# Replace with your actual API credentials
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Authenticate using OAuth 1.0a (most common)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create an API object
api = tweepy.API(auth)


def extract_tweets():
    try:
        # Verify credentials
        user = api.verify_credentials()
        print(f"Authentication successful! Logged in as: {user.screen_name}")
    except tweepy.TweepyException as e:
        print(f"Authentication failed: {e}")
        exit()

# List of Arabic news handles
# news_handles = ["AlArabiya", "AJArabic", "BBCArabic"]

# # Fetch recent tweets from each
# for handle in news_handles:
#     try:
#         tweets = api.user_timeline(screen_name=handle, count=10, tweet_mode="extended")
#         print(f"\nTweets from @{handle}:")
#         for tweet in tweets:
#             print(tweet.full_text)
#     except tweepy.TweepyException as e:
#         print(f"Error fetching tweets from @{handle}: {e}")


# Search for a hashtag or keyword
# query = "#الأخبار"
# try:
#     tweets = api.search_tweets(q=query, lang="ar", count=10, tweet_mode="extended")
#     print(f"\nTweets for {query}:")
#     for tweet in tweets:
#         print(tweet.full_text)
# except tweepy.TweepyException as e:
#     print(f"Error: {e}")


if __name__ == "__main__": 
    extract_tweets()