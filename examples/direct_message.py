"""
In this example i'm going to make a very simple code
to send messages to other user through DM
"""
import pytweet

client = pytweet.Client(
    "Your Bearer Token Here!!!",
    consumer_key="Your consumer_key here",
    consumer_key_secret="Your consumer_key_secret here",
    access_token="Your access_token here",
    access_token_secret="Your access_token_secret here",
)  # if you dont have one make an application in https://apps.twitter.com

try:
    user = client.fetch_user_by_name("SomeoneUserName")
    user.send(f"Hello World from {client.user}")
except Exception as e:
    raise e

else:
    print(f"Sent messages to {user.username}")

# You could also send a message to a tweet's author.

try:
    tweet = client.fetch_tweet("Tweet ID here")
    tweet.author.send(f"Hello World from {client.user}")
except Exception as e:
    raise e

else:
    print(f"Sent messages to {tweet.author.send}")
