:orphan:

.. currentmodule:: pytweet


Before Starting
====================================

Before using PyTweet you have to setup an application (https://apps.twitter.com). For a more comfortable experience, you can create an application inside a project. Most endpoints require the client to have `read`, `write` and `direct_messages` app permissions and elevated access type. 

For more accessibility you can create a dev environment to support events and other premium endpoints, you also need a web application url. We recommended ngrok for http tunneling, or make a flask application inside replit. You can make an https web application by just setting up a flask application and you get the web application's url! This requires you to install flask ``pip install Flask``.


Quickstart
====================================

This page is a simple and brief quickstart to pytweet!

A Basic PyTweet Client
----------------------------

To get start, let's make a simple twitter Client that fetch a user through its username, checkout the following code:

.. code-block:: python3

    import pytweet

    client = pytweet.Client(
        "Your Bearer Token Here!!!", 
        consumer_key="Your consumer key here", 
        consumer_secret="Your consumer secret here", 
        access_token="Your access token here", 
        access_token_secret="Your access token secret here",
    )

    user = client.fetch_user_by_username("TheGenocides")
    print(user.name, user.username, user.id)
    # Prints The user's name, username, and id

After that run your file!

Steps in our code
---------------------

1. We are importing pytweet using ``pytweet``
2. We are making our Client instance using ``client = pytweet.Client(...)``
3. We are fetching a user using ``client.fetch_user_by_username``
4. We are printing out the user name and ID


Implementing Events!
----------------------------

Now, comes the fun part. Pytweet has event handlers which you can use to make events, This requires you to make a Dev Environment and you also need a web application url, you can use replit for this one. To get the url you need to make a repl in replit and run a flask application, you will see a pop up with your web application's url, you also need to import ``Flask`` from ``flask`` using ``pip install Flask``. Here's a quick example from `example` folder:

.. code-block:: python3

    import pytweet
    from flask import Flask
    
    client = pytweet.Client(
        "Your Bearer Token Here!!!",
        consumer_key="Your consumer_key here",
        consumer_secret="Your consumer_secret here",
        access_token="Your access_token here",
        access_token_secret="Your access_token_secret here",
    )
    
    client.webapp = Flask(__name__)
    
    @client.event
    def on_direct_message(message: pytweet.DirectMessage):
        if message.author == client.account:
            return  # To avoid the client talking to itself.
    
        if message.text.lower() == "hello":
            message.author.send(f"Hello {message.author.username}!")
    
    
    client.listen(client.webapp, "YOUR_WEBAPP_URL", "YOUR_ENV_LABEL")
    
You can also use other events, currently there is more then 10 events that you can use. Here are some:

.. code-block:: python3

    @client.event
    def on_tweet_create(tweet): #An antonym for on_tweet_delete
        print(f"{tweet.author.username} Created a tweet: {tweet.url}")

    @client.event
    def on_user_follow(action): #An antonym for on_user_unfollow
        print(f"{action.author.username} Has followed {action.target.username}")

    @client.event
    def on_user_follow(action): #An antonym for on_user_unfollow
        print(f"{action.author.username} Has followed {action.target.username}")

    #More events...

Steps in our code
--------------------

1. We are importing pytweet using ``pytweet`` and Flask.
2. We are making our Client instance using ``client = pytweet.Client(...)``
3. We are setting an attribute to your client which is your web application through Flask.
4. We are making events using ``client.event`` decorator.
5. We are using ``client.listen`` for listening events send by twitter to your web application url.