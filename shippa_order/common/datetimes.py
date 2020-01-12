import time
from datetime import datetime, timezone
from types import MappingProxyType


def get_utc_datetime():
    """
        datetime.datetime(2020, 1, 11, 6, 59, 46, 684763, tzinfo=datetime.timezone.utc)

    :return: datetime for now
    :rtype: datetime.datetime
    """
    return datetime.fromtimestamp(time.time(), tz=timezone.utc)


DAYS = MappingProxyType({
    1: int('0000001', 2),
    2: int('0000010', 2),
    3: int('0000100', 2),
    4: int('0001000', 2),
    5: int('0010000', 2),
    6: int('0100000', 2),
    7: int('1000000', 2),
})


def get_day_from_datetime(datetime_):
    """
        return one of 1(SUN), 2(MON), 4(TUE), 8(WED), 16(THU), 32(FRI), 64(SAT)

    :param datetime_: datetime for getting day
    :return: day of input datetime_
    :rtype: int
    """
    return DAYS[datetime_.isoweekday()]


def get_time_from_datetime(datetime_):
    """
        datetime.time(7, 14, 2, 705418)

    :param datetime_: datetime for getting time
    :return: time of input datetime_
    :rtype: datetime.time
    """
    return datetime_.time()
