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


Twitter Models
---------------------

These following object are not meant to be create as an instance rather its for knowledge of what you can do with them.


User
~~~~~~~

.. attributetable:: User

.. autoclass:: User
    :members:

Tweet
~~~~~~~

.. attributetable:: Tweet

.. autoclass:: Tweet
    :members:

Space
~~~~~~~

.. attributetable:: Space

.. autoclass:: Space
    :members:


Messages
---------------------

These following object are not meant to be create as an instance rather its for knowledge of what you can do with them.

Message
~~~~~~~

.. attributetable:: Message

.. autoclass:: Message
    :members:

DirectMessage
~~~~~~~

.. attributetable:: DirectMessage

.. autoclass:: DirectMessage
    :members:


WelcomeMessage
~~~~~~~


.. attributetable:: WelcomeMessage

.. autoclass:: WelcomeMessage
    :members:


WelcomeMessageRule
~~~~~~~

.. attributetable:: WelcomeMessageRule

.. autoclass:: WelcomeMessageRule
    :members:


Attachments
---------------------

Attachments is a way to attach additional part to a message, this include tweet and direct message. You may contruct this following objects except :class:`CustomProfile`. Consider using :class:`client.create_custom_profile` for making a custom profile attachment.

CustomProfile
~~~~~~~

.. attributetable:: CustomProfile

.. autoclass:: CustomProfile
    :members:
    

Poll
~~~~~~~

.. attributetable:: Poll

.. autoclass:: Poll
    :members:


CTA
~~~~~~~

.. attributetable:: CTA

.. autoclass:: CTA
    :members:


QuickReply
~~~~~~~

.. attributetable:: QuickReply

.. autoclass:: QuickReply
    :members:


Geo
~~~~~~~

.. attributetable:: Geo

.. autoclass:: Geo
    :members:


File
~~~~~~~

.. attributetable:: File

.. autoclass:: File
    :members:




Streaming
---------------------

Streaming is a way to stream in twitter for tweets! This differ with `on_tweet_create`, Stream can detech global tweets while `on_tweet_create` only detech tweets from subscription users.

Stream
~~~~~~~

.. attributetable:: Stream

.. autoclass:: Stream
    :members:


StreamConnection
~~~~~~~

.. attributetable:: StreamConnection

.. autoclass:: StreamConnection
    :members:


StreamRule
~~~~~~~


.. attributetable:: StreamRule

.. autoclass:: StreamRule
    :members:

Relations
----------------

RelationFollow
~~~~~~~


.. attributetable:: RelationFollow

.. autoclass:: RelationFollow
    :members:

RelationLike
~~~~~~~

.. attributetable:: RelationLike

.. autoclass:: RelationLike
    :members:


RelationRetweet
~~~~~~~

.. attributetable:: RelationRetweet

.. autoclass:: RelationRetweet
    :members:


Embeds
----------------

Embed
~~~~~~~

.. attributetable:: Embed

.. autoclass:: Embed
    :members:


EmbedsImages
~~~~~~~

.. attributetable:: EmbedsImages


.. autoclass:: EmbedsImages
    :members:


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

Oauth is a way to authenticate a twitter user account. You can do this with the 3 legged authentication via :meth:`OauthSession.with_oauth_flow`. This also required in every request you've made for identification!

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

.. autoexception:: TooManyRequests

.. autoexception:: Forbidden


.. autoexception:: NotFound 
