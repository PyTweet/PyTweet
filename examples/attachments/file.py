"""
In this file im going to show you how you can attach file in a tweet. Using file is an easier way to interact with your audiences.
"""
import pytweet

client = pytweet.Client(
    "Your Bearer Token Here!!!",
    consumer_key="Your consumer_key here",
    consumer_key_secret="Your consumer_key_secret here",
    access_token="Your access_token here",
    access_token_secret="Your access_token_secret here",
)  # if you dont have one make an application in https://apps.twitter.com

file = pytweet.File("path/to/file", dm_only = False) 
#if its True dm_only enables the file to be send in user dm only. Default to False.

msg = client.tweet(f"Just setting up a bot to send a file.", file=file)
print(f"Posted tweet! https://twitter.com/{client.account.username}/status/{msg.id}")