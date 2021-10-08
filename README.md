# PyTweet

PyTweet is an api wrapper made for twitter using twitter's api version 2! 

# Usage

```py
import twitter

client=twitter.Client("Your Bearer Token Here!!!", consumer_key="Your consumer_key here", consumer_key_secret="Your consumer_key_secret here", access_token="Your access_token here", access_token_secret="Your access_token_secret here") #if you dont have one make an application in https://apps.twitter.com

user=client.get_user_by_username("TheGenocides")
print(user.name, user.username, user.id)
#Return The User's name, username, and id
