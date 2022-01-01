"""
A Simple twitter bot for responds commands using twitter account activity api (events)
Before making this simple bot, you have to create an environment in https://apps.twitter.com.
"""
import pytweet
from flask import Flask

client = pytweet.Client(
    "Your Bearer Token Here!!!",
    consumer_key="Your consumer_key here",
    consumer_secret="Your consumer_secret here",
    access_token="Your access_token here",
    access_token_secret="Your access_token_secret here",
)  # if you dont have one make an application in https://apps.twitter.com

client.webapp = Flask(__name__)


@client.event
def on_direct_message(message: pytweet.DirectMessage):
    if message.author == client.account:
        return  # To avoid the client talking to itself.

    if message.text.lower() == "hello":
        message.author.send(f"Hello {message.author.username}!")


client.listen(client.webapp, "YOUR_WEBAPP_URL", "YOUR_ENV_LABEL")
