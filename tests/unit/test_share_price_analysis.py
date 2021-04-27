import datetime as dt
import pytest
from src.app import SharePriceAnalysis


def test_validate_share_prices_not_list():
    with pytest.raises(ValueError) as error:
        # pylint: disable=protected-access
        SharePriceAnalysis._validate_share_prices("NOT_A_LIST")
    assert str(error.value) == "share_prices should be List of numbers"


def test_validate_shares_prices_with_only_one_value():
    with pytest.raises(ValueError) as error:
        # pylint: disable=protected-access
        SharePriceAnalysis._validate_share_prices([10])
    assert str(error.value) == "Need at least two values to compute the profit"


def test_validate_share_prices():
    try:
        # pylint: disable=protected-access
        SharePriceAnalysis._validate_share_prices([10, 20])
    # pylint: disable=bare-except
    except:
        pytest.fail("Unexpected Error")


def test_get_profit():
    # pylint: disable=protected-access
    result = SharePriceAnalysis._get_profit(10.2, 20)
    assert result == 9.8


def test_format_profit_details():
    share_prices = [10, 20]
    profit_details = {
        "max_profit": 10,
        "buy_position": 0,
        "sell_position": 1
    }
    start_time = dt.datetime.strptime("2021-04-26 10:00:00", '%Y-%m-%d %H:%M:%S')
    # pylint: disable=protected-access
    result = SharePriceAnalysis._format_profit_details(share_prices, profit_details, start_time)

    assert result == {
        "max_profit": profit_details["max_profit"],
        "buy_details": {
            "time": "2021-04-26 10:00:00",
            "value": 10
        },
        "sell_details": {
            "time": "2021-04-26 10:01:00",
            "value": 20
        }
    }


def test_format_profit_details_rounding_to_2_decimal():
    share_prices = [10, 20]
    profit_details = {
        "max_profit": 9.9999999999,
        "buy_position": 0,
        "sell_position": 1
    }
    start_time = dt.datetime.strptime("2021-04-26 10:00:00", '%Y-%m-%d %H:%M:%S')
    # pylint: disable=protected-access
    result = SharePriceAnalysis._format_profit_details(share_prices, profit_details, start_time)

    assert result == {
        "max_profit": 10,
        "buy_details": {
            "time": "2021-04-26 10:00:00",
            "value": 10
        },
        "sell_details": {
            "time": "2021-04-26 10:01:00",
            "value": 20
        }
    }


def test_get_max_profit_two_values():
    start_time = "2021-04-26 10:00:00"
    share_prices = [10.2, 20]
    result = SharePriceAnalysis.get_max_profit(start_time, share_prices)
    assert result == {
        "max_profit": 9.8,
        "buy_details": {
            "time": "2021-04-26 10:00:00",
            "value": 10.2
        },
        "sell_details": {
            "time": "2021-04-26 10:01:00",
            "value": 20
        }
    }


def test_get_max_profit_negative_profit():
    start_time = "2021-04-26 10:00:00"
    share_prices = [20, 10.2, 5.2]
    result = SharePriceAnalysis.get_max_profit(start_time, share_prices)
    assert result == {
        "max_profit": -5,
        "buy_details": {
            "time": "2021-04-26 10:01:00",
            "value": 10.2
        },
        "sell_details": {
            "time": "2021-04-26 10:02:00",
            "value": 5.2
        }
    }


def test_get_max_profit_multiple_profits():
    start_time = "2021-04-26 10:00:00"
    share_prices = [10, 7, 11, 5, 8]
    result = SharePriceAnalysis.get_max_profit(start_time, share_prices)
    assert result == {
        "max_profit": 4,
        "buy_details": {
            "time": "2021-04-26 10:01:00",
            "value": 7
        },
        "sell_details": {
            "time": "2021-04-26 10:02:00",
            "value": 11
        }
    }


def test_get_max_profit_multiple_same_profits():
    start_time = "2021-04-26 10:00:00"
    share_prices = [10, 7, 11, 5, 9]
    result = SharePriceAnalysis.get_max_profit(start_time, share_prices)
    assert result == {
        "max_profit": 4,
        "buy_details": {
            "time": "2021-04-26 10:01:00",
            "value": 7
        },
        "sell_details": {
            "time": "2021-04-26 10:02:00",
            "value": 11
        }
    }


def test_get_max_profit_large_profits():
    start_time = "2021-04-26 10:00:00"
    share_prices = [
        114, 95, 131, 22, 93, 57, 181, 158, 140, 62, 147, 21, 86,
        167, 96, 160, 39, 61, 20, 187, 178, 98, 153, 127, 193, 25,
        123, 64, 46, 67, 180, 170, 185, 149, 48, 99, 191, 87, 146,
        190, 53, 129, 105, 116, 11, 148, 79, 78, 26, 19, 82, 169,
        17, 14, 152, 124, 102, 186, 83, 179, 10, 173, 23, 183, 24,
        52, 172, 40, 100, 47, 34, 135, 85, 33, 182, 59, 144, 30, 43,
        28, 42, 138, 36, 45, 126, 192, 159, 139, 90, 56, 94, 143, 72,
        60, 18, 165, 80, 75, 112, 155, 188, 37, 197, 119, 130, 81, 150,
        125, 111, 49, 70, 133, 120, 44, 168, 145, 189, 66, 198, 41]

    result = SharePriceAnalysis.get_max_profit(start_time, share_prices)
    assert result == {
        "max_profit": 188,
        "buy_details": {
            "time": "2021-04-26 11:00:00",
            "value": 10
        },
        "sell_details": {
            "time": "2021-04-26 11:58:00",
            "value": 198
        }
    }
