"""
In this example i'm going to make a very simple code
to send messages to other user through DM
Code Explanations:
1. Wrap that the code in try-except block to make it easier to catch errors.
2. Fetch the user with get_user_by_username method.
3. Send a message to that user using the send method.
4. If it cause error and if the error is pytweet.errors.Forbidden it'll print the error. Other then pytweet.errors.Forbidden, it'll raise the errors. 
5. If it didnt cause any errors, it'll print success message.
"""
import pytweet

client = pytweet.Client(
    "Your Bearer Token Here!!!",
    consumer_key="Your consumer_key here",
    consumer_key_secret="Your consumer_key_secret here",
    access_token="Your access_token here",
    access_token_secret="Your access_token_secret here",
)  # if you dont have one make an application in https://apps.twitter.com

try:
    user=client.get_user_by_username("SomeoneUserName")
    user.send(f"Hello World from {client.user}")
except Exception as e:
    if isinstance(e, pytweet.errors.Forbidden):
        print("Cannot interact with that user! Return HTTP code 403: Forbidden!")

    else:
        raise e

else:
    print(f"Sent messages to {user.username}")