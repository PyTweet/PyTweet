.. currentmodule:: pytweet

API Reference
===============

The following section outlines the API of pytweet.

.. note::

    This module uses the Python logging module to log to tell you what you are doing wrong, See :doc:`logging` for more info.

Client
-------

.. attributetable:: Client

.. autoclass:: Client
    :members:


Commonly used Classes 
-------

There a lot of commonly used classes that is used frequently when using PyTweet, and here they are.

.. attributetable:: User

.. autoclass:: User
    :members:

.. attributetable:: UserPublicMetrics

.. autoclass:: UserPublicMetrics
    :members:

.. attributetable:: Tweet

.. autoclass:: Tweet
    :members:

.. attributetable:: TweetPublicMetrics


.. autoclass:: TweetPublicMetrics
    :members:

.. attributetable:: Message

.. autoclass:: Message
    :members:

.. attributetable:: DirectMessage

.. autoclass:: DirectMessage
    :members:

.. attributetable:: Media

.. autoclass:: Media
    :members:

.. attributetable:: Poll

.. autoclass:: Poll
    :members:

.. attributetable:: PollOptions

.. autoclass:: PollOptions
    :members:

.. attributetable:: RelationFollow

.. autoclass:: RelationFollow
    :members:

.. attributetable:: RelationLike

.. autoclass:: RelationLike
    :members:

.. attributetable:: RelationRetweet

.. autoclass:: RelationRetweet
    :members:

.. attributetable:: Embed

.. autoclass:: Embed
    :members:

.. attributetable:: EmbedsImages


.. autoclass:: EmbedsImages
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
