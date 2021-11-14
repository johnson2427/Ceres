import config
from ceres.backend.core.forcron import SqlConnection
from ceres.backend.api.tdameritrade import TDAmeritrade
from datetime import datetime
import pandas as pd


class OpeningRange(SqlConnection):

    def __init__(self):
        super().__init__(sql_host=config.HOST, sql_db=config.SQL_DB,
                         sql_user=config.SQL_USER, password=config.SQL_PASSWORD)

    def opening_range_breakout(self):
        self.cursor.execute(f"SELECT id FROM public.strategy WHERE name='opening_range_breakout'")
        strategy = self.cursor.fetchone()
        self.cursor.execute(f"SELECT symbol, name "
                            f"FROM public.stocks "
                            f"JOIN public.stock_strategy on public.stock_strategy.stock_id = stocks.id "
                            f"WHERE public.stock_strategy.strategy_id = %s", (strategy,))
        stocks = self.cursor.fetchall()
        date = "2021-11-05"
        start_minute_bar = f"{date} 09:30:00"
        start_minute_bar = datetime.strptime(start_minute_bar, "%Y-%m-%d %H:%M:%S")
        start_minute_bar = start_minute_bar.timestamp()*1000
        end_minute_bar = f"{date} 09:45:00"
        end_minute_bar = datetime.strptime(end_minute_bar, "%Y-%m-%d %H:%M:%S")
        end_minute_bar = end_minute_bar.timestamp() * 1000
        symbols = []
        for stock in stocks:
            symbols.append(stock[0])
        tda = TDAmeritrade(period_type='day', period='1', frequency_type='minute', frequency='1')
        for symbol in symbols:
            minute_bars = tda.get_prices(ticker=symbol)
            df = pd.DataFrame(minute_bars['candles'])
            opening_range_mask = df[df.datetime >= start_minute_bar]
            opening_range_mask = opening_range_mask[opening_range_mask.datetime < end_minute_bar]
            opening_range_low = opening_range_mask['low'].min()
            opening_range_high = opening_range_mask['high'].max()
            opening_range = opening_range_high-opening_range_low
            after_opening_range_mask = df[df.datetime >= end_minute_bar]
            after_opening_range_breakout = after_opening_range_mask[after_opening_range_mask['close'] >
                                                                    opening_range_high]
            if not after_opening_range_breakout.empty:
                limit_price = after_opening_range_breakout.iloc[0]['close']
                print(f"placing order for {symbol} at {limit_price}, closed_above {opening_range_high} at "
                      f"{after_opening_range_breakout.iloc[0]}")
                # Place order for stock here

    def opening_range_breakdown(self):
        self.cursor.execute(f"SELECT id FROM public.strategy WHERE name='opening_range_breakdown'")
        strategy = self.cursor.fetchone()
        self.cursor.execute(f"SELECT symbol, name "
                            f"FROM public.stocks "
                            f"JOIN public.stock_strategy on public.stock_strategy.stock_id = stocks.id "
                            f"WHERE public.stock_strategy.strategy_id = %s", (strategy,))
        stocks = self.cursor.fetchall()
        # check current orders
        date = "2021-11-05"
        start_minute_bar = f"{date} 09:30:00"
        start_minute_bar = datetime.strptime(start_minute_bar, "%Y-%m-%d %H:%M:%S")
        start_minute_bar = start_minute_bar.timestamp()*1000
        end_minute_bar = f"{date} 09:45:00"
        end_minute_bar = datetime.strptime(end_minute_bar, "%Y-%m-%d %H:%M:%S")
        end_minute_bar = end_minute_bar.timestamp() * 1000
        symbols = []
        for stock in stocks:
            symbols.append(stock[0])
        tda = TDAmeritrade(period_type='day', period='1', frequency_type='minute', frequency='1')
        for symbol in symbols:
            minute_bars = tda.get_prices(ticker=symbol)
            df = pd.DataFrame(minute_bars['candles'])
            opening_range_mask = df[df.datetime >= start_minute_bar]
            opening_range_mask = opening_range_mask[opening_range_mask.datetime < end_minute_bar]
            opening_range_low = opening_range_mask['low'].min()
            opening_range_high = opening_range_mask['high'].max()
            opening_range = opening_range_high-opening_range_low
            after_opening_range_mask = df[df.datetime >= end_minute_bar]
            after_opening_range_breakdown = after_opening_range_mask[after_opening_range_mask['close'] <
                                                                    opening_range_low]
            if not after_opening_range_breakdown.empty:
                limit_price = after_opening_range_breakdown.iloc[0]['close']
                print(f"placing order for {symbol} at {limit_price}, closed_above {opening_range_high} at "
                      f"{after_opening_range_breakdown.iloc[0]}")
                # Place order for stock here


if __name__ == "__main__":
    orb = OpeningRange()
    orb.opening_range_breakout()
