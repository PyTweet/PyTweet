"""
Here's another example of what you can make using pytweet, In Twitter i've seen a lot of giveaways fromm crypto to an item like iphone, computer etc. This is a giveaway function that is very easy to do using the user's followers! 
Code Explanation:
The client will get a user, from user we use the followers `property` then using time.sleep it make a delay then using random.choice it will pick one user from a list of users. 
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
    user = client.get_user_by_username("TheGenocides")
    followers = user.followers
    if followers == 0:  # Check if the user doesnt have a followers.
        return print("This user doesnt have a followers!")

    seconds = 60 * 3  # mark for 3 minutes, you can change to whatever minutes you like.
    print(
        f"Giveaway! there's a total of {len(followers)} users participate! Please wait for {seconds} seconds!"
    )

    time.sleep(seconds)
    winner = random.choice(followers)
    print(f"Giveaway Ended | Congrats! {winner.username} won the giveaway!")


if __name__ == "__main__":
    giveaway()
