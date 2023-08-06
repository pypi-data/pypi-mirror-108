from datetime import datetime

from sqlalchemy.types import TypeDecorator
from sqlalchemy.engine.interfaces import Dialect

from sqlalchemy.sql.sqltypes import (
    Boolean, Date, Integer, JSON, LargeBinary, NullType, String, Text,
)


class UnixTime(TypeDecorator):
    '''Seconds since epoch.
    '''
    impl = Integer
    exp = 0

    def process_bind_param(self, value: datetime, dialect: Dialect) -> int:
        return int(value.timestamp() * 10 ** self.exp)

    def process_result_value(self, value: int, dialect: Dialect) -> datetime:
        return datetime.fromtimestamp(value / 10 ** self.exp)


class UnixTimeMili(UnixTime):
    '''Miliseconds since epoch.
    '''
    exp = 3


class UnixTimeMicro(UnixTime):
    '''Nanoseconds since epoch.
    '''
    exp = 6


__all__ = [
    'Boolean',
    'Date',
    'Integer',
    'JSON',
    'LargeBinary',
    'NullType',
    'String',
    'Text',
    'UnixTime',
    'UnixTimeMili',
    'UnixTimeMicro',
]
