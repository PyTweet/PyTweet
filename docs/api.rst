.. currentmodule:: pytweet

API Reference
===============

The following section outlines the API of pytweet.

.. note::

    This module uses the Python logging module to log to tell you what you are doing wrong, See :doc:`logging` for more info.

Client
-------

.. autoclass:: Client
    :members:


Commonly used Classes 
-------

There a lot of comonly used classes that is used frequently when using PyTweet, and here they are.


.. autoclass:: User
    :members:

.. autoclass:: UserPublicMetrics
    :members:

.. autoclass:: Tweet
    :members:

.. autoclass:: TweetPublicMetrics
    :members:

.. autoclass:: Message
    :members:

.. autoclass:: DirectMessage
    :members:

.. autoclass:: Media
    :members:

.. autoclass:: Poll
    :members:


.. autoclass:: PollOptions
    :members:

.. autoclass:: RelationFollow
    :members:

.. autoclass:: RelationLike
    :members:

.. autoclass:: RelationRetweet
    :members:

.. autoclass:: Embed
    :members:

.. autoclass:: EmbedsImages
    :members:


Errors
-------

Error raised by pytweet.

.. autoexception::PytweetException

.. autoexception:: APIException


.. autoexception:: HTTPException

.. autoexception:: Unauthorized

.. autoexception:: TooManyRequests

.. autoexception:: Forbidden


.. autoexception:: NotFound 
