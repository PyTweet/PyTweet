"""
This is a simple code for getting user & Tweet's info.
"""
import pytweet

client = pytweet.Client(
    "Your Bearer Token Here!!!",
    consumer_key="Your consumer_key here",
    consumer_key_secret="Your consumer_key_secret here",
    access_token="Your access_token here",
    access_token_secret="Your access_token_secret here",
)  # if you dont have one make an application in https://apps.twitter.com


user = client.get_user_by_username("TheGenocides")
print(user.name, user.username, user.id)
# Return The user's name, username, and id

tweet = client.get_tweet("Tweet ID Here")
print(tweet.text, tweet.id, tweet.author.username)
# Return the tweet's text, id, and the author's username.
