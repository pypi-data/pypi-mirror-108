from __future__ import annotations
from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field, validator  # type: ignore

from .types import DbInteger, SensorType, SensorValueType


class Sensors(BaseModel):
    tag_id: DbInteger
    ts: datetime
    type: int
    value: SensorValueType

    @classmethod
    def from_row(cls, row):
        vals = dict(row)
        typ: SensorType = vals['type']
        if typ == SensorType.SensorDataTemp:
            return SensorDataTemp(**vals)
        if typ == SensorType.SensorDataHumid:
            return SensorDataHumid(**vals)
        return None


class SensorDataTemp(Sensors):
    type: int = Field(default=SensorType.SensorDataTemp, const=True)
    value: float

    @validator('value', pre=True)
    def convert_val(cls, v):
        return int.from_bytes(v, 'little', signed=True) / 10.0


class SensorDataHumid(Sensors):
    type: int = Field(default=SensorType.SensorDataHumid, const=True)
    value: int

    @validator('value', pre=True)
    def convert_val(cls, v):
        return int.from_bytes(v, 'little', signed=False)


AnySensor = Union[SensorDataTemp, SensorDataHumid]
