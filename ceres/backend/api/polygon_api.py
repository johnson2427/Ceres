import datetime
import time
import pandas as pd
from polygon import RESTClient, WebSocketClient, STOCKS_CLUSTER
import config


class PolygonWebSocket:

    def __init__(self):
        pass

    @staticmethod
    def my_custom_process_message(message):
        print("this is my custom message processing", message)

    @staticmethod
    def my_custom_error_handler(ws, error):
        print("this is my custom error handler", error)

    @staticmethod
    def my_custom_close_handler(ws):
        print("this is my custom close handler")

    def main(self):
        my_client = WebSocketClient(STOCKS_CLUSTER, config.POLYGON_API_KEY, self.my_custom_process_message)
        my_client.run_async()

        my_client.subscribe("T.MSFT", "T.AAPL", "T.AMD", "T.NVDA")
        time.sleep(1)

        my_client.close_connection()


class PolygonREST:

    def __init__(self):
        pass

    @staticmethod
    def ts_to_datetime(ts) -> str:
        return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')

    def main(self):
        key = config.POLYGON_API_KEY

        # RESTClient can be used as a context manager to facilitate closing the underlying http session
        # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
        with RESTClient(key) as client:
            from_ = "2021-01-01"
            to = "2021-11-01"
            resp = client.stocks_equities_aggregates("AAPL", 60, "minute", from_, to, unadjusted=False)

            print(f"Minute aggregates for {resp.ticker} between {from_} and {to}.")
            df = pd.DataFrame(resp.results)
            df['t'] = df['t'].apply(lambda x: self.ts_to_datetime(x))
            pass


if __name__ == "__main__":
    # poly = PolygonWebSocket()
    # poly.main()
    poly_rest = PolygonREST()
    poly_rest.main()
