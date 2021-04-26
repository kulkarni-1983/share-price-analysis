import json
import pytest

from src import app


@pytest.fixture()
def valid_event():
    return {
        "start_time": "2021-04-26 10:00:00",
        "share_prices": [10, 7, 11, 5, 8]
    }


def test_lambda_handler(valid_event, mocker):
    response = app.lambda_handler(valid_event, "")
    assert response["max_profit"] == 4
