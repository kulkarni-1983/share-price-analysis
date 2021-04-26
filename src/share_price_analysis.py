from util import get_time_str, format_start_time


class SharePriceAnalysis:

    @staticmethod
    def get_max_profit(start_time, share_prices):
        SharePriceAnalysis._validate_share_prices(share_prices)
        formatted_start_time = format_start_time(start_time)
        # initial values
        profit_details = {
            "max_profit": SharePriceAnalysis.get_profit(share_prices[0], share_prices[1]),
            "buy_position": 0,
            "sell_position": 1
        }
        # buy has to be before the sell
        # so assume the first position is the smallest value
        smallest_position = 0

        for current_position in range(1, len(share_prices)):
            current_profit = SharePriceAnalysis.get_profit(
                share_prices[smallest_position], share_prices[current_position])
            if current_profit > profit_details["max_profit"]:
                profit_details["max_profit"] = current_profit
                profit_details["buy_position"] = smallest_position
                profit_details["sell_position"] = current_position
            # update the smallest price if current price is lesser than the smallest
            if share_prices[current_position] < share_prices[smallest_position]:
                smallest_position = current_position

        return SharePriceAnalysis.format_profit_details(
            share_prices, profit_details, formatted_start_time)

    @staticmethod
    def format_profit_details(share_prices, profit_details, formatted_start_time):
        return {
            "max_profit": profit_details["max_profit"],
            "buy_details": {
                "time": get_time_str(formatted_start_time, profit_details["buy_position"]),
                "value": share_prices[profit_details["buy_position"]]
            },
            "sell_details": {
                "time": get_time_str(formatted_start_time, profit_details["sell_position"]),
                "value": share_prices[profit_details["sell_position"]]
            }
        }

    @staticmethod
    def get_profit(share_price_buy, share_price_sell):
        return share_price_sell - share_price_buy

    @staticmethod
    def _validate_share_prices(share_prices):
        if not isinstance(share_prices, list):
            raise RuntimeError("require share prices in List")
        if len(share_prices) <= 1:
            raise RuntimeError("Need at least two values to compute the profit")
