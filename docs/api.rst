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

Client
-------

.. attributetable:: Client

.. autoclass:: Client
    :members:


Commonly used Classes 
---------------------

There a lot of commonly used classes that is used frequently when using PyTweet, and here they are.

User
-------

.. attributetable:: User

.. autoclass:: User
    :members:

UserPublicMetrics
-------

.. attributetable:: UserPublicMetrics

.. autoclass:: UserPublicMetrics
    :members:

Tweet
-------

.. attributetable:: Tweet

.. autoclass:: Tweet
    :members:

TweetPublicMetrics
-------

.. attributetable:: TweetPublicMetrics

.. autoclass:: TweetPublicMetrics
    :members:

Message
-------

.. attributetable:: Message

.. autoclass:: Message
    :members:

DirectMessage
-------

.. attributetable:: DirectMessage

.. autoclass:: DirectMessage
    :members:

Media
-------

.. attributetable:: Media

.. autoclass:: Media
    :members:

Poll
-------

.. attributetable:: Poll

.. autoclass:: Poll
    :members:

.. attributetable:: PollOptions

.. autoclass:: PollOptions
    :members:

PollOptions
-------

.. attributetable:: RelationFollow

.. autoclass:: RelationFollow
    :members:

RelationLike
-------

.. attributetable:: RelationLike

.. autoclass:: RelationLike
    :members:

RelationReTweet
-------

.. attributetable:: RelationRetweet

.. autoclass:: RelationRetweet
    :members:

Embed
-------

.. attributetable:: Embed

.. autoclass:: Embed
    :members:


EmbedsImages
-------

.. attributetable:: EmbedsImages

.. autoclass:: EmbedsImages
    :members:


Errors
--------------------------

Error raised by pytweet.

.. autoexception:: PytweetException

.. autoexception:: APIException

.. autoexception:: HTTPException


.. autoexception:: Unauthorized

.. autoexception:: TooManyRequests

.. autoexception:: Forbidden


.. autoexception:: NotFound 
