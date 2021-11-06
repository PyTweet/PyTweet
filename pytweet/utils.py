import datetime
from typing import Any, Optional
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
