from dataclasses import dataclass
import pytz
from datetime import datetime

from shuttl_time.military_time import MilitaryTime
from shuttl_time.time_window import TimeWindow


@dataclass
class MilitaryTimeWindow:
    from_time: MilitaryTime
    to_time: MilitaryTime

    def __post_init__(self):
        assert self.from_time.tz == self.to_time.tz
        assert self.from_time < self.to_time

    @classmethod
    def from_json(cls, dikt: dict) -> "MilitaryTimeWindow":
        tz = pytz.timezone(dikt["timezone"])
        military_tw = cls(
            from_time=MilitaryTime(time=dikt["from_time"], tz=tz),
            to_time=MilitaryTime(time=dikt["to_time"], tz=tz),
        )
        return military_tw

    @property
    def tz(self) -> pytz.BaseTzInfo:
        return self.from_time.tz

    def to_json(self) -> dict:
        return {
            "from_time": self.from_time.time,
            "to_time": self.to_time.time,
            "timezone": str(self.from_time.tz),
        }

    def contains_datetime(self, dt: datetime) -> bool:
        local_dt = dt.astimezone(self.tz)
        military_time_dt = local_dt.hour * 100 + local_dt.minute
        return self.from_time.time <= military_time_dt <= self.to_time.time

    def get_military_tw_from_dt(self, dt: datetime) -> TimeWindow:
        fr_dt = self.from_time.combine(dt)
        to_dt = self.to_time.combine(dt)
        return TimeWindow(from_date=fr_dt, to_date=to_dt)
