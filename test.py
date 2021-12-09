import pytweet
import os

client=pytweet.Client(
    os.environ["bearer_token"], 
    consumer_key=os.environ["api_key"], 
    consumer_key_secret=os.environ["api_key_secret"], 
    access_token=os.environ["access_token"],
    access_token_secret=os.environ["access_token_secret"]
)

file = pytweet.File(open("images/LUKE.png", "rb"))
print(file.path)
# if its True dm_only enables the file to be send in user dm only. Default to False.

msg = client.tweet(f"Just setting up a bot to send a file.", file=file)
print(f"Posted tweet! https://twitter.com/{client.account.username}/status/{msg.id}")
