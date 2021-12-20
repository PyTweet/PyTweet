"""
Another example is a poll attachment. Twitter Polls are an easy way to interact with your audience, get creative, and understand people's opinions.
"""
import pytweet

client = pytweet.Client(
    "Your Bearer Token Here!!!",
    consumer_key="Your consumer_key here",
    consumer_secret="Your consumer_secret here",
    access_token="Your access_token here",
    access_token_secret="Your access_token_secret here",
)  # if you dont have one make an application in https://apps.twitter.com

poll = pytweet.Poll(duration=60)  # Set the duration to 60 minutes
poll.add_option(label="Pizza")
poll.add_option(label="Hamburger")
poll.add_option(label="Spaghetti")
msg = client.tweet("Here's a poll for yah! Which food do you like the most?", poll=poll)
print(f"Posted tweet! https://twitter.com/{client.account.username}/status/{msg.id}")
