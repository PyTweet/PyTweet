"""
Here's another example of what you can make using pytweet.
In Twitter i've seen a lot of giveaways from crypto to an item like iphone, computer etc. 
This is a very simple giveaway function using the user's followers! 
Code Explanation:
1. The client will fetch a user. 
2. from user we use the followers `property`.
3. then using time.sleep it make a delay.
4. then using random.choice it will pick one user from a list of users. 
"""
import pytweet
import time
import random

client = pytweet.Client(
    "Your Bearer Token Here!!!",
    consumer_key="Your consumer_key here",
    consumer_key_secret="Your consumer_key_secret here",
    access_token="Your access_token here",
    access_token_secret="Your access_token_secret here",
)  # if you dont have one make an application in https://apps.twitter.com


def giveaway():
    user = client.fetch_user_by_name("TheGenocides")  # 1
    followers = user.followers  # 2
    if len(followers) == 0:
        return print("This user doesnt have a followers!")

    seconds = 60 * 3
    print(
        f"Giveaway! there's a total of {len(followers)} users participate! Please wait for {seconds} seconds!"
    )

    time.sleep(seconds)  # 3
    winner = random.choice(followers)  # 4
    print(f"Giveaway Ended | Congrats! {winner.username} won the giveaway!")


if __name__ == "__main__":
    giveaway()
