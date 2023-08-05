from datetime import datetime

from pydantic import BaseModel  # type: ignore

from .types import DbInteger, SensorType, SensorValueType


class Sensors(BaseModel):
    tag_id: DbInteger
    ts: datetime
    type: SensorType
    value: SensorValueType

    @classmethod
    def from_row(cls, row):
        vals = dict(row)
        typ: SensorType = vals['type']
        print(typ)
        raw = vals['value']
        if typ == SensorType.SensorDataTemp:
            vals['value'] = \
                int.from_bytes(raw, 'little', signed=True) / 10.0
        if typ == SensorType.SensorDataHumid:
            vals['value'] = \
                int.from_bytes(raw, 'little', signed=False)
        return cls(**vals)
