from share_price_analysis import SharePriceAnalysis


def lambda_handler(event, context):
    try:
        return SharePriceAnalysis.get_max_profit(event["start_time"], event['share_prices'])
    except RuntimeError as error:
        # Return the error response
        return {
            "error": str(error)
        }


