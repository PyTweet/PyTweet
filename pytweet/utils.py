import datetime
from typing import Any, Optional, Union

from dateutil import parser


def time_parse_todt(date: Optional[Any]) -> datetime.datetime:
    """:class:`datetime.datetime`: Parse time return from twitter to datetime object!
    .. versionadded: 1.1.3
    """
    date = str(parser.parse(date))
    y, mo, d = date.split("-")
    h, mi, s = date.split(" ")[1].split("+")[0].split(":")

    return datetime.datetime(
        year=int(y),
        month=int(mo),
        day=int(d.split(" ")[0]),
        hour=int(h),
        minute=int(mi),
        second=int(s),
    )


def compose_tweet() -> str:
    """:class:`str`: Make a link that lets you compose a tweet

    .. versionadded: 1.3.5
    """
    return "https://twitter.com/intent/tweet"


def showcase_user(username: str):
    """:class:`str`: Make a link that lets you showcase user.

    Parameters
    ------------
    username: :class:`str`
        The user's username.

    .. versionadded: 1.3.5
    """
    return f"https://twitter.com/{username}"


def compose_tweet_action(tweet_id: Union[str, int], action: str):
    """:class:`str`: Make a link that lets you interact a tweet with certain actions.

    Parameters
    ------------
    tweet_id: Union[:class:`str`, :class:`int`]
        The tweet id you want to compose.
    action: str
        The action of a link.

    .. versionadded: 1.3.5
    """
    actions = ["retweet", "like", "reply"]
    if action.lower() not in actions:
        return TypeError("Action must be either 'retweet', 'like', or 'reply'")
    return (
        f"https://twitter.com/intent/{action}?tweet_id={tweet_id}"
        if action != "reply"
        else f"https://twitter.com/intent/tweet?in_reply_to={tweet_id}"
    )
