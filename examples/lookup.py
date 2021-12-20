"""
This is a simple code for user, tweet, space lookup!
"""
import pytweet

client = pytweet.Client(
    "Your Bearer Token Here!!!",
    consumer_key="Your consumer_key here",
    consumer_secret="Your consumer_secret here",
    access_token="Your access_token here",
    access_token_secret="Your access_token_secret here",
)  # if you dont have one make an application in https://apps.twitter.com


user = client.fetch_user_by_name("TheGenocides")
print(user.name, user.username, user.id)
# Returns The user's name, username, and id

tweet = client.fetch_tweet("The tweet id")  # Better to make this an int!
print(tweet.text, tweet.id, tweet.author.username)
# Returns the tweet's text, id, and the author's username.

space = client.fetch_space_by_title("Your Title Here")
print(space.state, space.id, space.host_id)
# Returns the space's state, id, and host's id. You can use fetch_user method to get the User object.
