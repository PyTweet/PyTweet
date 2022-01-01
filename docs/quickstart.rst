:orphan:

.. currentmodule:: pytweet

Quickstart
====================================

This page is a simple and brief quickstart to pytweet!

A Basic PyTweet Client
---------------

.. code-block:: python3

    import pytweet

    client = pytweet.Client(
        "Your Bearer Token Here!!!", 
        consumer_key="Your consumer key here", 
        consumer_secret="Your consumer secret here", 
        access_token="Your access token here", 
        access_token_secret="Your access token secret here",
    )
    #if you dont have one make an application in https://apps.twitter.com

    user = client.fetch_user_by_username("TheGenocides")
    print(user.name, user.username, user.id)
    # Return The user's name, username, and id

    tweet = client.fetch_tweet(Tweet ID Here)
    print(tweet.text, tweet.id, tweet.author.username)
    # Return the tweet's text, id, and the author's username.

Name this file ``pytweet_example.py``

Steps to running it
---------------

* Install pytweet, with ``pip install pytweet``

* Run ``python3 pytweet_example.py`` to run it.

Steps in our code
---------------

1. We are importing pytweet using ``pytweet``
2. We are making our Client instance using ``client = pytweet.Client(...)``
3. We are fetching a user using ``client.get_user_by_username``
4. We are printing out the user name and ID
5. We are fetching a tweet using ``client.get_tweet``
6. We are printing out the tweet's text, tweet's id and the tweet's author's name
