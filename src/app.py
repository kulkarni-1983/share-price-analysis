import datetime as dt


def lambda_handler(event, _):
    try:
        # Validate the received event
        if 'start_time' not in event or 'share_prices' not in event:
            raise ValueError("Event should have start_time and share_prices")
        # Compute max profit from the share prices
        return SharePriceAnalysis.get_max_profit(event['start_time'], event['share_prices'])
    except ValueError as error:
        # Return the error response
        return {
            "error": str(error)
        }


class SharePriceAnalysis:
    """
    Analysis the share price values to compute the maximum profit that can be achieved for list of
    share prices
    """
    @staticmethod
    def get_max_profit(start_time, share_prices):
        print("get_max_profit:", start_time, share_prices)
        SharePriceAnalysis._validate_share_prices(share_prices)
        formatted_start_time = TimeUtil.format_start_time(start_time)
        # initial values
        profit_details = {
            # Max profit can be negative
            "max_profit": SharePriceAnalysis._get_profit(share_prices[0], share_prices[1]),
            # buy before sell
            "buy_position": 0,
            "sell_position": 1
        }
        # buy has to be before the sell
        # so assume the first position is the smallest value
        smallest_position = 0

        for current_position in range(1, len(share_prices)):
            # difference between the smallest and the current position
            current_profit = SharePriceAnalysis._get_profit(
                share_prices[smallest_position], share_prices[current_position])

            # If the difference is more than the registered profit,
            # then use the current position as the max profit
            # also record the buy and sell positions
            if current_profit > profit_details["max_profit"]:
                profit_details["max_profit"] = current_profit
                profit_details["buy_position"] = smallest_position
                profit_details["sell_position"] = current_position

            # update the smallest price if current price is lesser than the smallest
            if share_prices[current_position] < share_prices[smallest_position]:
                smallest_position = current_position

        # Format the value to indicate the but and sell time as well
        return SharePriceAnalysis._format_profit_details(
            share_prices, profit_details, formatted_start_time)

    @staticmethod
    def _format_profit_details(share_prices, profit_details, formatted_start_time):
        return {
            "max_profit": round(profit_details["max_profit"], 2),
            "buy_details": {
                "time": TimeUtil.get_time_str(
                    formatted_start_time, profit_details["buy_position"]),
                "value": share_prices[profit_details["buy_position"]]
            },
            "sell_details": {
                "time": TimeUtil.get_time_str(
                    formatted_start_time, profit_details["sell_position"]),
                "value": share_prices[profit_details["sell_position"]]
            }
        }

    @staticmethod
    def _get_profit(share_price_buy, share_price_sell):
        return share_price_sell - share_price_buy

    @staticmethod
    def _validate_share_prices(share_prices):
        # share prices should be list having atleast two values
        if not isinstance(share_prices, list):
            raise ValueError("share_prices should be List of numbers")
        if len(share_prices) <= 1:
            raise ValueError("Need at least two values to compute the profit")


class TimeUtil:
    """
    Uses datetime to parse and format the time
    """
    @staticmethod
    def get_time_str(start_time, position_in_mins):
        if not isinstance(start_time, dt.datetime):
            raise ValueError("Expect start_time to be of type datetime")
        current_time = start_time + dt.timedelta(minutes=position_in_mins)
        return current_time.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def format_start_time(start_time):
        try:
            return dt.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        except ValueError as error:
            raise ValueError("Expect time in YYYY-MM-DD HH:MM:SS format") from error
