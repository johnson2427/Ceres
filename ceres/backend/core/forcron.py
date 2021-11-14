# import multiprocessing
import psycopg2
import pandas as pd
import numpy as np
import tulipy as ti
from ceres.backend.api.tdameritrade import TDAmeritrade, TDDataPull
import config
from datetime import datetime
from ceres.backend.db import database


class SqlConnection:

    def __init__(self, sql_host=config.HOST, sql_db=config.SQL_DB,
                 sql_user=config.SQL_USER, password=config.SQL_PASSWORD):
        self.conn = psycopg2.connect(f"host={sql_host} dbname={sql_db} user={sql_user} password={password}")
        self.cursor = self.conn.cursor()


class StockData(SqlConnection):

    def __init__(self):
        SqlConnection.__init__(self, sql_host=config.HOST, sql_db=config.SQL_DB,
                               sql_user=config.SQL_USER, password=config.SQL_PASSWORD)
        self.tda = TDAmeritrade()
        self.tddp = TDDataPull()
        self.db = database.SessionLocal()

    @staticmethod
    def get_stocks_from_db():
        df = pd.read_sql_table(table_name='stocks', con=database.engine)
        return df['symbol'].tolist()

    @staticmethod
    def get_stocks_df_from_db():
        df_stocks = pd.read_sql_table(table_name='stocks', con=database.engine)
        return df_stocks

    def drop_tables(self):
        self.cursor.execute(f"DROP TABLE public.fundamentals")
        self.cursor.execute(f"DROP TABLE public.prices")
        self.cursor.execute(f"DROP TABLE public.options")
        self.cursor.execute(f"DROP TABLE public.stocks")
        self.conn.commit()

    def get_stocks(self):
        stocks = self.tda.get_all_tickers()
        symbols = self.get_stocks_from_db()
        for stock in stocks:
            if stock not in symbols:
                try:
                    self.cursor.execute(f"INSERT INTO public.stocks(symbol, name) VALUES (%s, %s)", (stock, stocks[stock]))
                except Exception as err:
                    print(f"{err} for {stock} {stocks[stock]}")
                    self.conn.rollback()
                finally:
                    self.conn.commit()
                    print(f"Added a new stock {stock} {stocks[stock]}")

    def get_historical_prices(self, df_stocks, frequency):
        stocks = df_stocks['symbol'].tolist()
        for i, stock in enumerate(stocks):
            stock_id = df_stocks[df_stocks['symbol'] == stock]['id'][i]
            self.pull_and_store(stock, stock_id, frequency)

    def pull_and_store(self, ticker, ticker_id, frequency):
        try:
            price_data = self.pull_ticker(ticker, frequency)
            df_price = pd.DataFrame(price_data['candles'])
            df_price['stock_id'] = ticker_id
            df_price['interval'] = frequency
            df_price['datetime'] = [datetime.fromtimestamp(x / 1000) for x in df_price['datetime']]
            df_price = self.get_smas(df_price)
            df_price = self.get_bollinger(df_price)
            df_price['rsi14'] = self.get_rsi(df_price)
            df_price = self.get_macd(df_price)
            df_price.to_sql(name='prices_new', con=database.engine, if_exists='append', index=True, index_label='id')
        except Exception as err:
            print(f"{err} for {ticker}")
            if err.args[0] == 'candles':
                time.sleep(2)
                self.pull_and_store(ticker, ticker_id, frequency)
            else:
                pass

    def get_smas(self, df):
        if len(df) > 200:
            sma20 = np.append(np.zeros(19), ti.sma(np.array(df['close']), 20))
            sma50 = np.append(np.zeros(49), ti.sma(np.array(df['close']), 50))
            sma100 = np.append(np.zeros(99), ti.sma(np.array(df['close']), 100))
            sma200 = np.append(np.zeros(199), ti.sma(np.array(df['close']), 200))
        elif 100 < len(df) <= 200:
            sma20 = np.append(np.zeros(19), ti.sma(np.array(df['close']), 20))
            sma50 = np.append(np.zeros(49), ti.sma(np.array(df['close']), 50))
            sma100 = np.append(np.zeros(99), ti.sma(np.array(df['close']), 100))
            sma200 = np.zeros(len(df))
        elif 50 < len(df) <= 100:
            sma20 = np.append(np.zeros(19), ti.sma(np.array(df['close']), 20))
            sma50 = np.append(np.zeros(49), ti.sma(np.array(df['close']), 50))
            sma100 = np.zeros(len(df))
            sma200 = np.zeros(len(df))
        elif 20 < len(df) <= 50:
            sma20 = np.append(np.zeros(19), ti.sma(np.array(df['close']), 20))
            sma50 = np.zeros(len(df))
            sma100 = np.zeros(len(df))
            sma200 = np.zeros(len(df))
        else:
            sma20 = np.zeros(len(df))
            sma50 = np.zeros(len(df))
            sma100 = np.zeros(len(df))
            sma200 = np.zeros(len(df))
        df['sma20'] = sma20
        df['sma50'] = sma50
        df['sma100'] = sma100
        df['sma200'] = sma200
        return df

    def get_bollinger(self, df):
        if len(df) > 20:
            bb = np.zeros(19)
            lower, middle, upper = ti.bbands(np.array(df['close']), 20, 2)
            bb_lower = np.append(bb, lower)
            bb_middle = np.append(bb, middle)
            bb_upper = np.append(bb, upper)
        else:
            bb_lower = np.zeros(len(df))
            bb_middle = np.zeros(len(df))
            bb_upper = np.zeros(len(df))
        df['bb_lower'] = bb_lower
        df['bb_middle'] = bb_middle
        df['bb_upper'] = bb_upper
        return df

    def get_rsi(self, df):
        if len(df) > 14:
            return np.append(np.zeros(14), ti.rsi(np.array(df['close']), 14))
        else:
            return np.zeros(len(df))

    def get_macd(self, df):
        if len(df) > 26:
            macd, macd_signal, macd_histogram = ti.macd(np.array(df['close']), 12, 26, 9)
            macd = np.append(np.zeros(25), macd)
            macd_signal = np.append(np.zeros(25), macd_signal)
            macd_histogram = np.append(np.zeros(25), macd_histogram)
        else:
            macd = np.zeros(len(df))
            macd_signal = np.zeros(len(df))
            macd_histogram = np.zeros(len(df))
        df['macd'] = macd
        df['macd_signal'] = macd_signal
        df['macd_histogram'] = macd_histogram
        return df

    def pull_ticker(self, ticker, frequency):
        if frequency == 'daily':
            return self.tddp.pull_daily(ticker)
        elif frequency == 'one_minute':
            return self.tddp.pull_one_minute(ticker)
        elif frequency == 'five_minute':
            return self.tddp.pull_five_minute(ticker)
        elif frequency == 'ten_minute':
            return self.tddp.pull_ten_minute(ticker)
        elif frequency == 'fifteen_minute':
            return self.tddp.pull_fifteen_minute(ticker)
        elif frequency == 'thirty_minute':
            return self.tddp.pull_thirty_minute(ticker)
        elif frequency == 'one_hour':
            return self.tddp.pull_hour(ticker)
        elif frequency == 'weekly':
            return self.tddp.pull_weekly(ticker)

    def create_strategy(self, strategy):
        try:
            self.cursor.execute(f"INSERT INTO public.strategy(name) VALUES (%s)", (strategy,))
        except Exception as err:
            print(f"{err} adding {strategy}")
        finally:
            self.conn.commit()


if __name__ == "__main__":
    import time
    start = time.time()
    sd = StockData()
    # sd.get_stocks()
    df_stocks = sd.get_stocks_df_from_db()
    frequency = 'daily'
    sd.get_historical_prices(df_stocks, frequency)
    # p1 = multiprocessing.Process(target=sd.get_historical_prices, args=(df_stocks[0:1307], frequency))
    # p2 = multiprocessing.Process(target=sd.get_historical_prices,
    #                              args=(df_stocks[1307:2615].reset_index(drop=True), frequency))
    # p3 = multiprocessing.Process(target=sd.get_historical_prices,
    #                              args=(df_stocks[2615:3923].reset_index(drop=True), frequency))
    # p4 = multiprocessing.Process(target=sd.get_historical_prices,
    #                              args=(df_stocks[3923:5230].reset_index(drop=True), frequency))
    # p5 = multiprocessing.Process(target=sd.get_historical_prices,
    #                              args=(df_stocks[5230:6137].reset_index(drop=True), frequency))
    # p6 = multiprocessing.Process(target=sd.get_historical_prices,
    #                              args=(df_stocks[6137:7445].reset_index(drop=True), frequency))
    # p7 = multiprocessing.Process(target=sd.get_historical_prices,
    #                              args=(df_stocks[7445:9153].reset_index(drop=True), frequency))
    # p8 = multiprocessing.Process(target=sd.get_historical_prices,
    #                              args=(df_stocks[9153:10460].reset_index(drop=True), frequency))
    # p1.start()
    # p2.start()
    # p3.start()
    # p4.start()
    # p5.start()
    # p6.start()
    # p7.start()
    # p8.start()
    # p1.join()
    # p2.join()
    # p3.join()
    # p4.join()
    # p5.join()
    # p6.join()
    # p7.join()
    # p8.join()
    print("Done")
    # sd.get_historical_prices(df_stocks, 'daily')
    end = time.time()
    time = end-start
    print(time)
    # sd.create_strategy("opening_range_breakout")
    # sd.create_strategy("opening_range_breakdown")
