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

These following object are not meant to be create as an instance rather its for knowledge of what you can do with them.

Media
~~~~~~~


.. attributetable:: Media

.. autoclass:: Media
    :members:


Poll
~~~~~~~

.. attributetable:: Poll

.. autoclass:: Poll
    :members:



PollOption
~~~~~~~


.. attributetable:: PollOption

.. autoclass:: PollOption
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


Button
~~~~~~~


.. attributetable:: Button

.. autoclass:: Button
    :members:

Option
~~~~~~~


.. attributetable:: Option

.. autoclass:: Option
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
