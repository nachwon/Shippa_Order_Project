from types import MappingProxyType
from enum import IntEnum


class UserLevelCodes(IntEnum):
    is_superuser = 10000
    is_staff = 1000
    is_active = 100


class BinaryOfDays(IntEnum):
    SUN = int('1000000', 2)
    MON = int('0100000', 2)
    TUE = int('0010000', 2)
    WED = int('0001000', 2)
    THU = int('0000100', 2)
    FRI = int('0000010', 2)
    SAT = int('0000001', 2)


def _available_days(business_day):
    days = [(64, 'SUN', ), (32, 'MON', ), (16, 'TUE', ), (8, 'WED', ),
            (4, 'THU', ), (2, 'FRI', ), (1, 'SAT', ), ]
    return [day for binary, day in days if binary & business_day]


MAPPING_OF_AVAILABLE_DAYS = MappingProxyType({
    business_day: _available_days(business_day)
    for business_day in range(1, 128)
})

AVAILABLE_COUNTRY_ISO_LIST = ['KR', ]

AVAILABLE_CURRENCIES = ['KRW', ]
