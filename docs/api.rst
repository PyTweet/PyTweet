.. currentmodule:: pytweet

API Reference
===============

The following section outlines the API of pytweet.

.. note::

    This module uses the Python logging module to log to tell you what you are doing wrong, See :doc:`logging` for more info.

Version Related Info
---------------------

.. data:: version_info

    A named tuple that is similar to :obj:`py:sys.version_info`.

.. data:: __version__

    Get the version of the module (e.g ``1.0.0`` or ``1.0.0a``) this is based on :pep:`440`.


Classes 
---------------------------

These are all the **public** classes of pytweet.

Clients
----------------

Client
~~~~~~~

.. attributetable:: Client

.. autoclass:: Client
    :members:

Application
----------------

ApplicationInfo
~~~~~~~


.. autoclass:: ApplicationInfo()
    :members:

Environment
----------------

Webhook
~~~~~~~

.. autoclass:: Webhook()
    :members:

Environment
~~~~~~~

.. autoclass:: Environment()
    :members:


Twitter Models
---------------------

These following object are not meant to be create as an instance rather its for knowledge of what you can do with them.


User
~~~~~~~

.. autoclass:: User()
    :members:

ClientAccount
~~~~~~~

.. autoclass:: ClientAccount()
    :members:
    :inherited-members:

Tweet
~~~~~~~

.. autoclass:: Tweet()
    :members:
    :inherited-members:

Space
~~~~~~~

.. autoclass:: Space()
    :members:


Message
~~~~~~~

.. autoclass:: Message()
    :members:

DirectMessage
~~~~~~~

.. autoclass:: DirectMessage()
    :members:
    :inherited-members:


WelcomeMessage
~~~~~~~


.. autoclass:: WelcomeMessage()
    :members:
    :inherited-members:


WelcomeMessageRule
~~~~~~~

.. autoclass:: WelcomeMessageRule()
    :members:


Attachments
---------------------

Attachments is a way to attach additional part to a message, this include tweet and direct message. You may contruct this following objects except :class:`CustomProfile`. Consider using :class:`Client.create_custom_profile` for making a custom profile attachment.

CustomProfile
~~~~~~~

.. autoclass:: CustomProfile
    :members:
    

Poll
~~~~~~~

.. autoclass:: Poll()
    :members:


CTA
~~~~~~~

.. autoclass:: CTA()
    :members:


QuickReply
~~~~~~~

.. autoclass:: QuickReply()
    :members:


Geo
~~~~~~~

.. autoclass:: Geo()
    :members:


File
~~~~~~~

.. autoclass:: File()
    :members:




Streaming
---------------------

Streaming is a way to stream in twitter for tweets! This differ with `on_tweet_create`, Stream can detech global tweets while `on_tweet_create` only detech tweets from subscription users.

Stream
~~~~~~~

.. autoclass:: Stream()
    :members:


StreamConnection
~~~~~~~

.. autoclass:: StreamConnection()
    :members:


StreamRule
~~~~~~~

.. autoclass:: StreamRule
    :members:

Relations
----------------

Relations is an object that returns from a user action or a tweet action. This include but not limited to: :class:`Tweet.like`, :class:`Tweet.retweet`, :class:`Tweet.hide`, and :class:`User.follow`.

RelationFollow
~~~~~~~

.. autoclass:: RelationFollow()
    :members:


RelationLike
~~~~~~~

.. autoclass:: RelationLike()
    :members:


RelationRetweet
~~~~~~~

.. autoclass:: RelationRetweet()
    :members:


RelationHide
~~~~~~~

.. autoclass:: RelationHide()
    :members:


Embeds
----------------

The embedded urls object returned by :class:`Tweet.embeds`.

Embed
~~~~~~~

.. autoclass:: Embed()
    :members:


EmbedsImages
~~~~~~~

.. autoclass:: EmbedsImages()
    :members:


Entities
----------------

Objects derives from entities.py

Hashtags
~~~~~~~

.. autoclass:: Hashtags()
    :members:

UserMentions
~~~~~~~

.. autoclass:: UserMentions()
    :members:

Urls
~~~~~~~

.. autoclass:: Urls(()
    :members:

Symbols
~~~~~~~

.. autoclass:: Symbols()
    :members:

Media
~~~~~~~

.. autoclass:: Media()
    :members:


Event Objects
----------------

Event objects are objects returned by an event filled with the event data.

Event
~~~~~~~

.. autoclass:: Event()
    :members:

DirectMessageEvent
~~~~~~~

.. autoclass:: DirectMessageEvent()
    :members:
    :inherited-members:

UserActionEvent
~~~~~~~

.. autoclass:: UserActionEvent()
    :members:
    :inherited-members:

DirectMessageTypingEvent
~~~~~~~

.. autoclass:: DirectMessageTypingEvent()
    :members:
    :inherited-members:

DirectMessageReadEvent
~~~~~~~

.. autoclass:: DirectMessageReadEvent()
    :members:
    :inherited-members:

TweetFavoriteActionEvent
~~~~~~~

.. autoclass:: TweetFavoriteActionEvent()
    :members:
    :inherited-members:

UserFollowActionEvent
~~~~~~~

.. autoclass:: UserFollowActionEvent()
    :members:
    :inherited-members:

UserUnfollowActionEvent
~~~~~~~

.. autoclass:: UserUnfollowActionEvent()
    :members:
    :inherited-members:

UserBlockActionEvent
~~~~~~~

.. autoclass:: UserBlockActionEvent()
    :members:
    :inherited-members:

UserUnblockActionEvent
~~~~~~~

.. autoclass:: UserUnblockActionEvent()
    :members:
    :inherited-members:

UserMuteActionEvent
~~~~~~~

.. autoclass:: UserMuteActionEvent()
    :members:
    :inherited-members:

UserUnmuteActionEvent
~~~~~~~

.. autoclass:: UserUnmuteActionEvent()
    :members:
    :inherited-members:


.. _twitter-api-events:

Event Reference
---------------------
This section shows events listened to by :class:`Client`

You can register an event using :meth:`Client.event`

Example:

.. code-block:: python

  @client.event
  def on_stream_connect(connection):
   print(connection)


.. function:: on_stream_connect(connection)

    `on_stream_connect` is an event triggered when the client succesfuly connect to stream, this might trigger multiple times as a reconnect logic would trigger this event too.

    :param connection: The Stream connection.
    :type connection: :class:`StreamConnection`

.. function:: on_stream_disconnect(connection)

    `on_stream_disconnect` is an event triggered when the client disconnect from stream.

    :param connection: The Stream connection.
    :type connection: :class:`StreamConnection` 

.. function:: on_stream(tweet, connection)

    `on_stream` is an event triggered when a stream return a tweet data.

    :param tweet: The data that’s going to be returns from the stream.
    :param connection: The stream connection
    :type tweet: :class:`Tweet`
    :type connection: :class:`StreamConnection`

.. function:: on_tweet_create(tweet)

    `on_tweet_create` is an event triggered when a subscription user created a tweet.

    :param tweet: The :class:`Tweet` that created by a subscription user.
    :type tweet: :class:`Tweet`

.. function:: on_tweet_delete(tweet)

    `on_tweet_delete` is an event triggered when a subscription user deleted a tweet.

    :param tweet: The :class:`Tweet` that deleted by a subscription user.
    :type tweet: :class:`Tweet`

.. function:: on_tweet_favorite(action)

    `on_tweet_favorite` is an event triggered when someone liked the subscription user's tweet.

    :param action: The event action object information.
    :type action: :class:`TweetFavoriteActionEvent`

.. function:: on_user_follow(action)

    `on_user_follow` is an event triggered when someone follows the subscription user or the subscription user follows someone.

    :param action: The event action object information.
    :type action: :class:`UserFollowActionEvent`

.. function:: on_user_unfollow(action)

    `on_user_unfollow` is an event triggered when someone unfollows the subscription user.

    :param action: The event action object information.
    :type action: :class:`UserUnfollowActionEvent`

.. function:: on_user_block(action)

    `on_user_block` is an event triggered when someone blocks the subscription user.

    :param action: The event action object information.
    :type action: :class:`UserBlockActionEvent`

.. function:: on_user_unblock(action)

    `on_user_unblock` is an event triggered when someone unblocks the subscription user.

    :param action: The event action object information.
    :type action: :class:`UserUnblockActionEvent`

.. function:: on_user_mute(action)

    `on_user_mute` is an event triggered when someone mutes the subscription user.

    :param action: The event action object information.
    :type action: :class:`UserMuteActionEvent`

.. function:: on_user_unmute(action)

    `on_user_unmute` is an event triggered when someone unmutes the subscription user.

    :param action: The event action object information.
    :type action: :class:`UserUnmuteActionEvent`

.. function:: on_direct_message(message)

    `on_direct_message` is an event triggered when someone send a message to the subscription user or from the the subscription user. 

    :param message: The :class:`DirectMessage` that the subscription user sent or from the the subscription user.
    :type message: :class:`DirectMessage`

.. function:: on_direct_message_read(action)

    `on_direct_message_read` is an event triggered when someone read messages in the subscription user's dm.

    :param action: The event action object information.
    :type action: :class:`DirectMessageReadEvent`

.. function:: on_typing(action)

    `on_typing` is an event triggered when someone trigger a typing animation in the subscription user dm.

    :param action: The event action object information.
    :type action: :class:`DirectMessageTypingEvent`

Enums 
--------------

All these enums are a subclass of :class:`enum.Enum`

.. class:: SpaceState

    .. attribute:: live

        indicates the space is live
    

    .. attribute:: scheduled

        indicates the space is scheduled
    

.. class:: ReplySetting

    .. attribute:: everyone

        Everyone can reply.
    

    .. attribute:: mention_users

        Only users who are mentioned in the tweet can reply.
    

    .. attribute:: following

        Only people who are following the author of the tweet can reply.

.. class:: MessageTypeEnum

    .. attribute:: DIRECT_MESSAGE

        A direct message in twitter.
    

    .. attribute:: MESSAGE_TWEET

        A public tweet.
    

    .. attribute:: MESSAGE_WELCOME_MESSAGE

        A welcome message in a direct message.
    

    .. attribute:: MESSAGE_WELCOME_MESSAGE_RULE

        A welcome message rule in a direct message.


Oauth
-------------

Oauth is a way to authenticate a twitter user account. You can do this with 3 legged authentication via :meth:`OauthSession.generate_oauth_url` to generate an oauth url and :meth:`OauthSession.post_oauth_token` to post an oauth token and verifier. This also required in every request you've made for identification!

OauthSession
~~~~~~~

.. attributetable:: OauthSession


.. autoclass:: OauthSession
    :members:


Errors
-------

Error raised by pytweet.

.. autoexception:: PytweetException

.. autoexception:: APIException

.. autoexception:: HTTPException


.. autoexception:: Unauthorized

.. autoexception:: BadRequests

.. autoexception:: TooManyRequests

.. autoexception:: Forbidden

.. autoexception:: Conflict

.. autoexception:: ConnectionException

.. autoexception:: FieldsTooLarge


.. autoexception:: NotFound 
