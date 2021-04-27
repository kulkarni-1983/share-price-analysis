import datetime as dt
import pytest
from src.app import TimeUtil


def test_get_time_str():
    start_time = dt.datetime.strptime("2021-04-26 10:00:00", '%Y-%m-%d %H:%M:%S')
    result = TimeUtil.get_time_str(start_time, 20)
    assert result == "2021-04-26 10:20:00"


def test_get_time_str_adds_hours_if_min_greater_than_60():
    start_time = dt.datetime.strptime("2021-04-26 10:00:00", '%Y-%m-%d %H:%M:%S')
    result = TimeUtil.get_time_str(start_time, 90)
    assert result == "2021-04-26 11:30:00"


def test_get_time_str_negative_time():
    start_time = dt.datetime.strptime("2021-04-26 10:00:00", '%Y-%m-%d %H:%M:%S')
    result = TimeUtil.get_time_str(start_time, -20)
    assert result == "2021-04-26 09:40:00"


def test_get_time_str_invalid_start_time():
    start_time = "invalid_date_time"
    with pytest.raises(ValueError) as error:
        TimeUtil.get_time_str(start_time, 20)
    assert str(error.value) == "Expect start_time to be of type datetime"


def test_format_start_time():
    start_time_str = "2021-04-26 10:00:00"
    result = TimeUtil.format_start_time(start_time_str)
    assert result.strftime('%Y-%m-%d %H:%M:%S') == start_time_str


def test_format_start_time_raises_on_invalid_format():
    invalid_time = "2021-04-26 __invalid__"
    with pytest.raises(ValueError) as error:
        TimeUtil.format_start_time(invalid_time)
    assert str(error.value) == "Expect time in YYYY-MM-DD HH:MM:SS format"
