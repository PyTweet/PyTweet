# PyTweet

PyTweet is an api wrapper made for twitter using twitter's api version 2! 

# Usage

```py
import twitter

client=twitter.Client(token="Your Bearer Token Here!!!") #if you dont have one make an application in https://apps.twitter.com

user=client.get_user_by_username("TheGenocides")
print(user.name, user.username, user.id)
#Return The User's name, username, and id
```