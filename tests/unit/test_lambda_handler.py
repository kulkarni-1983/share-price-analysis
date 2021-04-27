from src import app


def test_lambda_handler(mocker):
    event = {
        "start_time": "2021-04-26 10:00:00",
        "share_prices": [10, 7, 11, 5, 8]
    }
    expected = {
        "max_profit": 4
    }
    get_max_profit_mock = mocker.patch('src.app.SharePriceAnalysis.get_max_profit')
    get_max_profit_mock.return_value = expected
    response = app.lambda_handler(event, "")
    assert response == expected
    get_max_profit_mock.assert_called_once_with(event["start_time"], event["share_prices"])


def test_lambda_handler_no_start_time():
    event = {
        "share_prices": [10, 20]
    }

    response = app.lambda_handler(event, "")
    assert response["error"] == "Event should have start_time and share_prices"


def test_lambda_handler_no_share_prices():
    event = {
        "start_time": "some_time"
    }

    response = app.lambda_handler(event, "")
    assert response["error"] == "Event should have start_time and share_prices"
