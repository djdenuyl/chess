"""
Time util functions

author: David den Uyl (djdenuyl@gmail.com)
date: 2023-03-19
"""
from datetime import datetime, time, timedelta
from typing import Union


def countdown(time_: str, as_datetime: bool = False) -> Union[datetime, str]:
    """ countdown a time-str of format <MM:SS> to 0 seconds. returns one second less than given time or 00:00 if
     time has run out. if as_datetime is True, returns a datetime object, else a str. defaults to False """
    new_time = t - timedelta(seconds=1) if (t := datetime.strptime(time_, '%M:%S')) != time() else time()

    if as_datetime:
        return new_time

    return new_time.strftime('%M:%S')


def time_int_to_str(value: int) -> str:
    return (datetime.min + timedelta(seconds=value)).strftime('%M:%S')
