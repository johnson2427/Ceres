import psycopg2
from tdameritrade import TDAmeritrade
import config
from datetime import datetime
import alpaca_trade_api as atradeapi


class SqlConnection:

    def __init__(self, sql_host=config.HOST, sql_db=config.SQL_DB,
                 sql_user=config.SQL_USER, password=config.SQL_PASSWORD):
        self.conn = psycopg2.connect(f"host={sql_host} dbname={sql_db} user={sql_user} password={password}")
        self.cursor = self.conn.cursor()


class StockData(TDAmeritrade, SqlConnection):

    def __init__(self):
        TDAmeritrade.__init__(self, api_key=config.tda_api_key, period_type='year', period='1', frequency_type='daily',
                              frequency='1', projection='fundamental', direction='up', change='percent')
        SqlConnection.__init__(self, sql_host=config.HOST, sql_db=config.SQL_DB,
                               sql_user=config.SQL_USER, password=config.SQL_PASSWORD)

    def get_stocks_from_db(self):
        self.cursor.execute(f"SELECT symbol, name FROM public.stocks")
        rows = self.cursor.fetchall()
        symbols = [row[0] for row in rows]
        return symbols

    def get_stocks_dict_from_db(self):
        self.cursor.execute(f"SELECT id, symbol, name FROM public.stocks")
        rows = self.cursor.fetchall()
        stock_dict = {}
        for row in rows:
            stock_dict[row[1]] = row[0]
        return stock_dict

    def drop_tables(self):
        self.cursor.execute(f"DROP TABLE public.fundamentals")
        self.cursor.execute(f"DROP TABLE public.prices")
        self.cursor.execute(f"DROP TABLE public.options")
        self.cursor.execute(f"DROP TABLE public.stocks")
        self.conn.commit()

    def get_stocks(self):
        stocks = self.get_all_tickers()
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

    def get_historical_prices_alpaca(self, interval):
        symbols_dict = self.get_stocks_dict_from_db()
        symbols = list(symbols_dict.keys())
        api = atradeapi.REST(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY, base_url=config.ALPACA_ENDPOINT)
        chunk_size = 200
        for i in range(0, len(symbols), chunk_size):
            symbol_chunk = symbols[i:i+chunk_size]
            barsets = api.get_barset(symbol_chunk, interval)
            for symbol in barsets:
                print(f"processing stock {symbol}")
                for bar in barsets[symbol]:
                    stock_id = symbols_dict[symbol]
                    try:
                        self.cursor.execute(f"INSERT INTO public.prices_new(stock_id, interval, date_time, open, "
                                            f"high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                            (int(stock_id), interval, bar.t.strftime('%Y-%m-%d %H:%M:%S.%f'), bar.o,
                                             bar.h, bar.l, bar.c, bar.v))
                    except Exception as err:
                        print(f"{err} for {symbol} {interval} {bar.t.strftime('%Y-%m-%d %H:%M:%S.%f')}")
                        self.conn.rollback()
                    finally:
                        self.conn.commit()
                        print(f"Added a new stock {symbol} {interval} {bar.t.strftime('%Y-%m-%d %H:%M:%S.%f')}")

    def get_historical_prices(self):
        stocks_dict = self.get_stocks_dict_from_db()
        for key in stocks_dict.keys():
            stock = stocks_dict[key]
            price_data = self.get_prices(stock)
            for elem in price_data['candles']:
                open = float(elem['open'])
                high = float(elem['high'])
                low = float(elem['low'])
                close = float(elem['close'])
                volume = int(elem['volume'])
                date_time = datetime.fromtimestamp(int(elem['datetime'])/1000).strftime("%m-%d-%Y %H:%M:%S")
                date_time = datetime.strptime(date_time, "%m-%d-%Y %H:%M:%S")
                try:
                    self.cursor.execute(f"INSERT INTO public.prices(stock_id, interval, date_time, open, high, low, "
                                        f"close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (int(key),
                                                                                                    self.frequency_type,
                                                                                                    date_time, open,
                                                                                                    high, low, close,
                                                                                                    volume))
                except Exception as err:
                    print(f"{err} for {stock} {self.frequency_type} {date_time}")
                    self.conn.rollback()
                finally:
                    self.conn.commit()
                    print(f"Added a new stock {stock} {self.frequency_type} {date_time}")

    def create_strategy(self, strategy):
        try:
            self.cursor.execute(f"INSERT INTO public.strategy(name) VALUES (%s)", (strategy,))
        except Exception as err:
            print(f"{err} adding {strategy}")
        finally:
            self.conn.commit()


if __name__ == "__main__":
    sd = StockData()
    # sd.get_stocks()
    # sd.get_historical_prices()
    sd.create_strategy("opening_range_breakout")
    sd.create_strategy("opening_range_breakdown")
