import json

from share_price_analysis import SharePriceAnalysis


def lambda_handler(event, context):

    try:
        return SharePriceAnalysis(event["start_time"]).get_max_profit(event['src'])
    except RuntimeError as error:
        # Return the error response
        return {
            "error": str(error)
        }
