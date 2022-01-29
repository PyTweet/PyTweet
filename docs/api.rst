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


Clients
----------------

Client
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Client
    :members:


Application
----------------

ApplicationInfo
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ApplicationInfo()
    :members:


Environment
----------------

Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Environment()
    :members:

Webhook
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Webhook()
    :members:


Twitter Models
---------------------

These following objects are not meant to be create as an instance rather its for knowledge of what you can do with them.


User
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: User()
    :members:


Tweet
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Tweet()
    :members:
    :inherited-members:


Space
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Space()
    :members:


List
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: List()
    :members:


ClientAccount
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ClientAccount()
    :members:
    :inherited-members:


Message
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Message()
    :members:

DirectMessage
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: DirectMessage()
    :members:
    :inherited-members:


WelcomeMessage
~~~~~~~~~~~~~~~~~~~~~~~~~~


.. autoclass:: WelcomeMessage()
    :members:
    :inherited-members:


WelcomeMessageRule
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: WelcomeMessageRule()
    :members:


Twitter Dataclass
-------------------------

These following section documented objects that use `dataclasses.dataclass` decorator.

Attachments Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: PollOption
    :members:

.. autoclass:: Option
    :members:

.. autoclass:: Button
    :members:

Locations Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Location
    :members:

.. autoclass:: Trend
    :members:

.. autoclass:: PlaceType
    :members:

.. autoclass:: TimezoneInfo
    :members:

Settings Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserSettings
    :members:

.. autoclass:: SleepTimeSettings
    :members:

Space Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: SpaceTopic
    :members:

Stream Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: StreamRule
    :members:


Attachments
---------------------

Attachments is a way to attach additional part to a message, this include tweet and direct message. You may contruct this following objects except :class:`CustomProfile` and :class:`Geo`. Consider using :class:`Client.create_custom_profile` for making a custom profile attachment and :class:`Client.search_geo` for searching a geo-location.

CustomProfile
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: CustomProfile
    :members:
    

Poll
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Poll()
    :members:


CTA
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: CTA()
    :members:


QuickReply
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: QuickReply()
    :members:


Geo
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Geo()
    :members:


Files
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: File()
    :members:


SubFile
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: SubFile()
    :members:


Streaming
---------------------

Streaming is a way to stream in twitter for tweets! This differ with `on_tweet_create`, Stream can detech global tweets while `on_tweet_create` only detech tweets from subscription users.

Stream
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Stream()
    :members:


StreamConnection
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: StreamConnection()
    :members:


Oauth
-------------

Oauth is a way to authenticate a twitter user account. You can do this with 3 legged authentication via :meth:`OauthSession.generate_oauth_url` to generate an oauth url and :meth:`OauthSession.post_oauth_token` to post an oauth token and verifier. This also required in every request you've made for identification! This section will show you what you can do with oauth, You can use `Client.http.oauth_session` to get the client's `OauthSession`.

OauthSession
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: OauthSession
    :members:

Scope
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Scope
    :members:


Pagination
-------------

Some endpoints returns more objects but limits it to some pages. Using pagination classes like `UserPagination` and `TweetPagination`, you can change page and manage objects easily. Example:

.. code-block:: py

    pagination = client.account.fetch_following()
    print("Page 1, object 1:", pagination.content[0])
    pagination.next_page() #Change page to the next page
    print("Page 2, object 2:", pagination.content[1])
    pagination.previous_page() #Change page to the previous page
    print("Page 1, object 3:", pagination.content[2])

    #since the pagination caches page content everytime you turn pages, you can do this:
    for page_number, page_content in pagination.pages:
        print(f"Page {page_number}, object: 1: {page_content[0]}")


Pagination
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Pagination
    :members:

UserPagination
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserPagination
    :members:
    :inherited-members:

TweetPagination
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: TweetPagination
    :members:
    :inherited-members:



Relations
----------------

Relations is an object that returns from a user action or a tweet action. This include but not limited to: :class:`Tweet.like`, :class:`Tweet.retweet`, :class:`Tweet.hide`, and :class:`User.follow`.

RelationFollow
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: RelationFollow()
    :members:


RelationLike
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: RelationLike()
    :members:


RelationRetweet
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: RelationRetweet()
    :members:


RelationHide
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: RelationHide()
    :members:


Embeds
----------------

The embedded urls object returned by :class:`Tweet.embeds`.

Embed
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Embed()
    :members:


EmbedsImages
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: EmbedsImages()
    :members:


Entities
----------------

Objects derives from entities.py

Hashtag
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Hashtag()
    :members:

UserMention
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserMention()
    :members:

Url
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Url()
    :members:

Symbol
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Symbol()
    :members:

Media
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Media()
    :members:


Event Objects
----------------

Event objects are objects returned by an event filled with the event data.

Event
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Event()
    :members:

DirectMessageEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: DirectMessageEvent()
    :members:
    :inherited-members:

UserActionEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserActionEvent()
    :members:
    :inherited-members:

DirectMessageTypingEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: DirectMessageTypingEvent()
    :members:
    :inherited-members:

DirectMessageReadEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: DirectMessageReadEvent()
    :members:
    :inherited-members:

TweetFavoriteActionEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: TweetFavoriteActionEvent()
    :members:
    :inherited-members:

UserFollowActionEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserFollowActionEvent()
    :members:
    :inherited-members:

UserUnfollowActionEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserUnfollowActionEvent()
    :members:
    :inherited-members:

UserBlockActionEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserBlockActionEvent()
    :members:
    :inherited-members:

UserUnblockActionEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserUnblockActionEvent()
    :members:
    :inherited-members:

UserMuteActionEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserMuteActionEvent()
    :members:
    :inherited-members:

UserUnmuteActionEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserUnmuteActionEvent()
    :members:
    :inherited-members:


.. _twitter-api-events:

Event Reference
---------------------
This section shows events listened to by :class:`Client`. You can register an event using :meth:`Client.event`

Example:

.. code-block:: python

    @client.event
    def on_tweet_create(tweet):
        print(f"Someone posted a tweet: {tweet}")


.. function:: on_stream_connect(connection)

    `on_stream_connect` is an event triggers when the client succesfuly connect to stream, this might trigger multiple times as a reconnect logic would trigger this event too.

    :param connection: The Stream connection.
    :type connection: :class:`StreamConnection`

.. function:: on_stream_disconnect(connection)

    `on_stream_disconnect` is an event triggers when the client disconnect from stream.

    :param connection: The Stream connection.
    :type connection: :class:`StreamConnection` 

.. function:: on_stream(tweet, connection)

    `on_stream` is an event triggers when a stream return a tweet data.

    :param tweet: The data that’s going to be returns from the stream.
    :param connection: The stream connection
    :type tweet: :class:`Tweet`
    :type connection: :class:`StreamConnection`

.. function:: on_tweet_create(tweet)

    `on_tweet_create` is an event triggers when a subscription user created a tweet.

    :param tweet: The :class:`Tweet` that created by a subscription user.
    :type tweet: :class:`Tweet`

.. function:: on_tweet_delete(tweet)

    `on_tweet_delete` is an event triggers when a subscription user deleted a tweet.

    :param tweet: The :class:`Tweet` that deleted by a subscription user.
    :type tweet: :class:`Tweet`

.. function:: on_tweet_favorite(action)

    `on_tweet_favorite` is an event triggers when someone likes/favorites the subscription user's tweet.

    :param action: The event action object information.
    :type action: :class:`TweetFavoriteActionEvent`

.. function:: on_user_follow(action)

    `on_user_follow` is an event triggers when someone follows the subscription user or the subscription user follows someone.

    :param action: The event action object information.
    :type action: :class:`UserFollowActionEvent`

.. function:: on_user_unfollow(action)

    `on_user_unfollow` is an event triggers when someone unfollows the subscription user.

    :param action: The event action object information.
    :type action: :class:`UserUnfollowActionEvent`

.. function:: on_user_block(action)

    `on_user_block` is an event triggers when someone blocks the subscription user.

    :param action: The event action object information.
    :type action: :class:`UserBlockActionEvent`

.. function:: on_user_unblock(action)

    `on_user_unblock` is an event triggers when someone unblocks the subscription user.

    :param action: The event action object information.
    :type action: :class:`UserUnblockActionEvent`

.. function:: on_user_mute(action)

    `on_user_mute` is an event triggers when someone mutes the subscription user.

    :param action: The event action object information.
    :type action: :class:`UserMuteActionEvent`

.. function:: on_user_unmute(action)

    `on_user_unmute` is an event triggers when someone unmutes the subscription user.

    :param action: The event action object information.
    :type action: :class:`UserUnmuteActionEvent`

.. function:: on_direct_message(message)

    `on_direct_message` is an event triggers when someone send a message to the subscription user or from the the subscription user. 

    :param message: The :class:`DirectMessage` that the subscription user sent or from the the subscription user.
    :type message: :class:`DirectMessage`

.. function:: on_direct_message_read(action)

    `on_direct_message_read` is an event triggers when someone read messages in the subscription user's dm.

    :param action: The event action object information.
    :type action: :class:`DirectMessageReadEvent`

.. function:: on_typing(action)

    `on_typing` is an event triggers when someone trigger a typing animation in the subscription user dm.

    :param action: The event action object information.
    :type action: :class:`DirectMessageTypingEvent`

Enums 
--------------

All these enums are a subclass of :class:`enum.Enum`

.. class:: MessageTypeEnum

    .. attribute:: DIRECT_MESSAGE

        A direct message in twitter.
    

    .. attribute:: MESSAGE_TWEET

        A public tweet.
    

    .. attribute:: MESSAGE_WELCOME_MESSAGE

        A welcome message in a direct message.
    

    .. attribute:: MESSAGE_WELCOME_MESSAGE_RULE

        A welcome message rule in a direct message.

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

.. class:: ButtonType

    .. attribute:: web_url

        A button type for opening a url.


.. class:: ActionEventType

    .. attribute:: direct_message_read

        A direct message read action event, this action event type returns by `on_direct_message_read` through the :meth:`Event.type` attribute.


    .. attribute:: direct_message_typing

        A direct message typing action event, this action event type returns by `on_typing`.


.. class:: UserActionEventType

    .. attribute:: follow

        A user follow action type returns by `on_user_follow` and `on_user_unfollow`.


    .. attribute:: block

        A user block action type returns by `on_user_block` and `on_user_unblock`.


    .. attribute:: mute

        A user mute action type returns by `on_user_mute` and `on_user_unmute`.


.. class:: Timezone

    .. attribute:: international_dateline_west

        A timezone for Etc/GMT.
        

    .. attribute:: midway_island

        A timezone for Pacific/Midway.
        

    .. attribute:: american_samoa

        A timezone for Pacific/Pago_Pago.
        

    .. attribute:: hawaii

        A timezone for Pacific/Honolulu.
        

    .. attribute:: alaska

        A timezone for America/Juneau.
        

    .. attribute:: pacific_time

        A timezone for America/Los_Angeles.
        

    .. attribute:: tijuana

        A timezone for America/Tijuana.
        

    .. attribute:: mountain_time

        A timezone for America/Denver.
        

    .. attribute:: arizona

        A timezone for America/Phoenix.
        

    .. attribute:: chihuahua

        A timezone for America/Chihuahua.
        

    .. attribute:: mazatlan

        A timezone for America/Mazatlan.
        

    .. attribute:: central_time

        A timezone for America/Chicago.
        

    .. attribute:: saskatchewan

        A timezone for America/Regina.
        

    .. attribute:: guadalajara

        A timezone for America/Mexico_City.
        

    .. attribute:: mexicoCity

        A timezone for America/Mexico_City.
        

    .. attribute:: monterrey

        A timezone for America/Monterrey.
        

    .. attribute:: central_america

        A timezone for America/Guatemala.
        

    .. attribute:: eastern_time

        A timezone for America/New_York.
        

    .. attribute:: indiana

        A timezone for America/Indiana.
        

    .. attribute:: bogota

        A timezone for America/Bogota.
        

    .. attribute:: lima

        A timezone for America/Lima.
        

    .. attribute:: quito

        A timezone for America/Lima.
        

    .. attribute:: atlantic_time

        A timezone for America/Halifax.
        

    .. attribute:: caracas

        A timezone for America/Caracas.
        

    .. attribute:: lapaz

        A timezone for America/La_Paz.
        

    .. attribute:: santiago

        A timezone for America/Santiago.
        

    .. attribute:: newfoundland

        A timezone for America/St_Johns.
        

    .. attribute:: brasilia

        A timezone for America/Sao_Paulo.
        

    .. attribute:: buenos_aires

        A timezone for America/Argentina.
        

    .. attribute:: montevideo

        A timezone for America/Montevideo.
        

    .. attribute:: georgetown

        A timezone for America/Guyana.
        

    .. attribute:: puerto_rico

        A timezone for America/Puerto_Rico.
        

    .. attribute:: greenland

        A timezone for America/Godthab.
        

    .. attribute:: mid_atlantic

        A timezone for Atlantic/South_Georgia.
        

    .. attribute:: azores

        A timezone for Atlantic/Azores.
        

    .. attribute:: cape_verde

        A timezone for Atlantic/Cape_Verde.
        

    .. attribute:: dublin

        A timezone for Europe/Dublin.
        

    .. attribute:: edinburgh

        A timezone for Europe/London.
        

    .. attribute:: lisbon

        A timezone for Europe/Lisbon.
        

    .. attribute:: london

        A timezone for Europe/London.
        

    .. attribute:: casablanca

        A timezone for Africa/Casablanca.
        

    .. attribute:: monrovia

        A timezone for Africa/Monrovia.
        

    .. attribute:: utc

        A timezone for Etc/UTC.
        

    .. attribute:: belgrade

        A timezone for Europe/Belgrade.
        

    .. attribute:: bratislava

        A timezone for Europe/Bratislava.
        

    .. attribute:: budapest

        A timezone for Europe/Budapest.
        

    .. attribute:: ljubljana

        A timezone for Europe/Ljubljana.
        

    .. attribute:: prague

        A timezone for Europe/Prague.
        

    .. attribute:: sarajevo

        A timezone for Europe/Sarajevo.
        

    .. attribute:: skopje

        A timezone for Europe/Skopje.
        

    .. attribute:: warsaw

        A timezone for Europe/Warsaw.
        

    .. attribute:: zagreb

        A timezone for Europe/Zagreb.
        

    .. attribute:: brussels

        A timezone for Europe/Brussels.
        

    .. attribute:: copenhagen

        A timezone for Europe/Copenhagen.
        

    .. attribute:: madrid

        A timezone for Europe/Madrid.
        

    .. attribute:: paris

        A timezone for Europe/Paris.
        

    .. attribute:: amsterdam

        A timezone for Europe/Amsterdam.
        

    .. attribute:: berlin

        A timezone for Europe/Berlin.
        

    .. attribute:: bern

        A timezone for Europe/Zurich.
        

    .. attribute:: zurich

        A timezone for Europe/Zurich.
        

    .. attribute:: rome

        A timezone for Europe/Rome.
        

    .. attribute:: stockholm

        A timezone for Europe/Stockholm.
        

    .. attribute:: vienna

        A timezone for Europe/Vienna.
        

    .. attribute:: westCentralAfrica

        A timezone for Africa/Algiers.
        

    .. attribute:: bucharest

        A timezone for Europe/Bucharest.
        

    .. attribute:: cairo

        A timezone for Africa/Cairo.
        

    .. attribute:: helsinki

        A timezone for Europe/Helsinki.
        

    .. attribute:: kyiv

        A timezone for Europe/Kiev.
        

    .. attribute:: riga

        A timezone for Europe/Riga.
        

    .. attribute:: sofia

        A timezone for Europe/Sofia.
        

    .. attribute:: tallinn

        A timezone for Europe/Tallinn.
        

    .. attribute:: vilnius

        A timezone for Europe/Vilnius.
        

    .. attribute:: athens

        A timezone for Europe/Athens.
        

    .. attribute:: istanbul

        A timezone for Europe/Istanbul.
        

    .. attribute:: minsk

        A timezone for Europe/Minsk.
        

    .. attribute:: jerusalem

        A timezone for Asia/Jerusalem.
        

    .. attribute:: harare

        A timezone for Africa/Harare.
        

    .. attribute:: pretoria

        A timezone for Africa/Johannesburg.
        

    .. attribute:: kaliningrad

        A timezone for Europe/Kaliningrad.
        

    .. attribute:: moscow

        A timezone for Europe/Moscow.
        

    .. attribute:: StPetersburg

        A timezone for Europe/Moscow.
        

    .. attribute:: volgograd

        A timezone for Europe/Volgograd.
        

    .. attribute:: samara

        A timezone for Europe/Samara.
        

    .. attribute:: kuwait

        A timezone for Asia/Kuwait.
        

    .. attribute:: riyadh

        A timezone for Asia/Riyadh.
        

    .. attribute:: nairobi

        A timezone for Africa/Nairobi.
        

    .. attribute:: baghdad

        A timezone for Asia/Baghdad.
        

    .. attribute:: tehran

        A timezone for Asia/Tehran.
        

    .. attribute:: abuDhabi

        A timezone for Asia/Muscat.
        

    .. attribute:: muscat

        A timezone for Asia/Muscat.
        

    .. attribute:: baku

        A timezone for Asia/Baku.
        

    .. attribute:: tbilisi

        A timezone for Asia/Tbilisi.
        

    .. attribute:: yerevan

        A timezone for Asia/Yerevan.
        

    .. attribute:: kabul

        A timezone for Asia/Kabul.
        

    .. attribute:: ekaterinburg

        A timezone for Asia/Yekaterinburg.
        

    .. attribute:: islamabad

        A timezone for Asia/Karachi.
        

    .. attribute:: karachi

        A timezone for Asia/Karachi.
        

    .. attribute:: tashkent

        A timezone for Asia/Tashkent.
        

    .. attribute:: chennai

        A timezone for Asia/Kolkata.
        

    .. attribute:: kolkata

        A timezone for Asia/Kolkata.
        

    .. attribute:: mumbai

        A timezone for Asia/Kolkata.
        

    .. attribute:: newDelhi

        A timezone for Asia/Kolkata.
        

    .. attribute:: kathmandu

        A timezone for Asia/Kathmandu.
        

    .. attribute:: astana

        A timezone for Asia/Dhaka.
        

    .. attribute:: dhaka

        A timezone for Asia/Dhaka.
        

    .. attribute:: sriJayawardenepura

        A timezone for Asia/Colombo.
        

    .. attribute:: almaty

        A timezone for Asia/Almaty.
        

    .. attribute:: novosibirsk

        A timezone for Asia/Novosibirsk.
        

    .. attribute:: rangoon

        A timezone for Asia/Rangoon.
        

    .. attribute:: bangkok

        A timezone for Asia/Bangkok.
        

    .. attribute:: hanoi

        A timezone for Asia/Bangkok.
        

    .. attribute:: jakarta

        A timezone for Asia/Jakarta.
        

    .. attribute:: krasnoyarsk

        A timezone for Asia/Krasnoyarsk.
        

    .. attribute:: beijing

        A timezone for Asia/Shanghai.
        

    .. attribute:: chongqing

        A timezone for Asia/Chongqing.
        

    .. attribute:: hongKong

        A timezone for Asia/Hong_Kong.
        

    .. attribute:: urumqi

        A timezone for Asia/Urumqi.
        

    .. attribute:: kualaLumpur

        A timezone for Asia/Kuala_Lumpur.
        

    .. attribute:: singapore

        A timezone for Asia/Singapore.
        

    .. attribute:: taipei

        A timezone for Asia/Taipei.
        

    .. attribute:: perth

        A timezone for Australia/Perth.
        

    .. attribute:: irkutsk

        A timezone for Asia/Irkutsk.
        

    .. attribute:: ulaanbaatar

        A timezone for Asia/Ulaanbaatar.
        

    .. attribute:: seoul

        A timezone for Asia/Seoul.
        

    .. attribute:: osaka

        A timezone for Asia/Tokyo.
        

    .. attribute:: sapporo

        A timezone for Asia/Tokyo.
        

    .. attribute:: tokyo

        A timezone for Asia/Tokyo.
        

    .. attribute:: yakutsk

        A timezone for Asia/Yakutsk.
        

    .. attribute:: darwin

        A timezone for Australia/Darwin.
        

    .. attribute:: adelaide

        A timezone for Australia/Adelaide.
        

    .. attribute:: canberra

        A timezone for Australia/Melbourne.
        

    .. attribute:: melbourne

        A timezone for Australia/Melbourne.
        

    .. attribute:: sydney

        A timezone for Australia/Sydney.
        

    .. attribute:: brisbane

        A timezone for Australia/Brisbane.
        

    .. attribute:: hobart

        A timezone for Australia/Hobart.
        

    .. attribute:: vladivostok

        A timezone for Asia/Vladivostok.
        

    .. attribute:: guam

        A timezone for Pacific/Guam.
        

    .. attribute:: portMoresby

        A timezone for Pacific/Port_Moresby.
        

    .. attribute:: magadan

        A timezone for Asia/Magadan.
        

    .. attribute:: srednekolymsk

        A timezone for Asia/Srednekolymsk.
        

    .. attribute:: solomon

        A timezone for Pacific/Guadalcanal.
        

    .. attribute:: newCaledonia

        A timezone for Pacific/Noumea.
        

    .. attribute:: fiji

        A timezone for Pacific/Fiji.
        

    .. attribute:: kamchatka

        A timezone for Asia/Kamchatka.
        

    .. attribute:: marshall

        A timezone for Pacific/Majuro.
        

    .. attribute:: auckland

        A timezone for Pacific/Auckland.
        

    .. attribute:: wellington

        A timezone for Pacific/Auckland.
        

    .. attribute:: nukualofa

        A timezone for Pacific/Tongatapu.
        

    .. attribute:: tokelau

        A timezone for Pacific/Fakaofo.
        

    .. attribute:: chatham

        A timezone for Pacific/Chatham.
        

    .. attribute:: samoa

        A timezone for Pacific/Apia.
        

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

.. autoexception:: UnKnownSpaceState

.. autoexception:: NoPageAvailable 