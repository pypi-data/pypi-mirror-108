from enum import Enum
from typing import Dict, Union

from pydantic import ConstrainedInt

Attributes = Dict[str, Union[str, int, bytes]]


class DbInteger(ConstrainedInt):
    min = 0
    max = 2**31 - 1


class Unsigned32Bit(ConstrainedInt):
    ge = 0
    lt = 2**32


class Unsigned16Bit(Unsigned32Bit):
    lt = 2**16


SensorValueType = Union[float, int]


class SensorType(str, Enum):
    SensorDataTemp = 'SensorDataTemp'
    SensorDataHumid = 'SensorDataHumid'


__all__ = ['Attributes', 'DbInteger', 'Unsigned16Bit', 'Unsigned32Bit',
           'SensorType', 'SensorValueType']
