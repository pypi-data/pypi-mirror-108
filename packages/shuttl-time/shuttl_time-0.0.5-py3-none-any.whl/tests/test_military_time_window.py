import pytest
import pytz
from datetime import datetime

from tests.factories import military_time_window_dm

from shuttl_time import MilitaryTimeWindow, MilitaryTime


class TestSMilitaryTimeWindow:
    def test_from_json_and_to_json(self):
        military_tw = military_time_window_dm()
        military_tw2 = MilitaryTimeWindow.from_json(military_tw.to_json())
        assert military_tw.from_time == military_tw2.from_time
        assert military_tw.to_time == military_tw2.to_time
        assert military_tw.tz == military_tw2.tz

    @pytest.mark.xfail(strict=True)
    def test_init_fails_on_from_time_greater_than_to_time(self):
        MilitaryTimeWindow(from_time=1000, to_time=500)

    def test_get_military_time_window_from_dt(self):
        military_tw = military_time_window_dm()
        time_window = military_tw.get_military_tw_from_dt(
            dt=datetime(2021, 1, 1, 10, 10)
        )
        assert (
            MilitaryTime.extract_from_datetime(time_window.from_date)
            == military_tw.from_time
        )
        assert (
            MilitaryTime.extract_from_datetime(time_window.to_date)
            == military_tw.to_time
        )
        assert military_tw.contains_datetime(
            dt=time_window.from_date
        ) and military_tw.contains_datetime(dt=time_window.to_date)

    def test_contains_datetime(self):
        tz_utc = pytz.utc
        tz_in = pytz.timezone("Asia/Kolkata")
        military_tw = military_time_window_dm(1000, 1500, timezone=tz_utc)
        assert military_tw.contains_datetime(
            dt=tz_utc.localize(datetime(2021, 1, 1, 12, 0))
        )
        assert not military_tw.contains_datetime(
            dt=tz_utc.localize(datetime(2021, 1, 1, 17, 0))
        )
        assert military_tw.contains_datetime(
            dt=tz_in.localize(datetime(2021, 1, 1, 17, 0))
        )
