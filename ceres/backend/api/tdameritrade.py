import requests
import json
import config
from datetime import datetime
from yahoo_fin import stock_info as si


class TDAmeritrade:
    """
    Pulls stock data from TD Ameritrade API

    stock_ticker: str -> stock ticker you are looking for data for
    api_key: str -> in the config file, this is the API key to TD Ameritrade
    period_type: str -> day, month, year, or ytd, default is year
    period: str -> The number of periods to show, default is 1
    frequency_type: str -> minute, daily, weekly or monthly. Default is daily
    frequency: str -> if minute (put 1, 5, 10, 15, 30), if daily (put 1), if weekly (put 1), if monthly (put 1)
    need_extended: str -> get extended hours data with true
    projection: str -> type of information you are looking for from fundamentals. Default is fundamental
    TO BE ADDED FOR OPTIONS
    contract_type: str -> CALL, PUT or ALL. Default is ALL
    strike_count: str -> The number of strikes to return above and below the at the money price. Default is 10
    include_quotes: str -> Include quotes for options in the option chain. Can be TRUE or FALSE. Default is TRUE
    strategy: str -> SINGLE, ANALYTICAL (Allows use of volatility, underlyingPrice, InterestRate, and daysToExpire
                     params to calculate theoretical values), COVERED, VERTICAL, CALENDAR, STRANGLE, STRADDLE,
                     BUTTERFLY, CONDOR, DIAGONAL, COLLAR, or ROLL. Default is SINGLE
    strike: str -> strike price, Default 10 -> MUST PUT A VALUE IN FOR THIS
    option_range -> ITM (In The Money), NTM (Near the Money), OTM (Out of the money), SAK (Strikes Above Market),
                    SBK (Strikes Below Market), SNK (Strikes Near Market), ALL (All Strikes) Default ALL
    from_date
    to_date
    volatility
    underlying_price
    interest_rate
    days_to_expire
    exp_month
    option_type
    """

    def __init__(self, api_key=config.tda_api_key, period_type='year', frequency_type='daily', frequency='1',
                 projection='fundamental', direction='up', change='percent', start_date='2020-01-01',
                 end_date=datetime.today()):
        self.api_key = api_key
        self.period_type = period_type
        self.frequency_type = frequency_type
        self.frequency = frequency
        self.projection = projection
        self.direction = direction
        self.change = change
        self.start_date = str(int(datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000))
        self.end_date = str(int(end_date.timestamp() * 1000))
        # self.end_date = str(int(datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000))

    @staticmethod
    def get_all_tickers():
        df1 = si.tickers_dow(include_company_data=True)
        df1 = df1[['Symbol', 'Company']]
        df2 = si.tickers_sp500(include_company_data=True)
        df2 = df2[['Symbol', 'Security']]
        df2.rename(columns={'Security': 'Company'}, inplace=True)
        df3 = si.tickers_nasdaq(include_company_data=True)
        df3 = df3[['Symbol', 'Security Name']]
        df3.rename(columns={'Security Name': 'Company'}, inplace=True)
        df4 = si.tickers_other(include_company_data=True)
        df4 = df4[['ACT Symbol', 'Security Name']]
        df4.rename(columns={'ACT Symbol': 'Symbol', 'Security Name': 'Company'}, inplace=True)
        df = df1.append(df2).append(df3).append(df4)
        df.sort_values(by='Symbol', inplace=True)
        df.drop_duplicates(subset="Symbol", keep="first", inplace=True)
        df = df[~df['Symbol'].str.contains('.', regex=False)]
        df = df[~df['Symbol'].str.contains('$', regex=False)]
        df = df[df['Symbol'] != 'ZVV']
        df = df[df['Symbol'] != 'ZVZZC']
        df = df[df['Symbol'] != 'ZVZZT']
        df = df[df['Symbol'] != 'ZWZZT']
        df = df[df['Symbol'] != 'ZXZZT']
        df = df[df['Symbol'] != 'ZJZZT']
        df = df[~df["Symbol"].str.contains("File Creation")]
        return df.set_index('Symbol')['Company'].to_dict()

    def get_prices(self, ticker):
        price_endpoint = config.prices_url.format(stock_ticker=ticker,
                                                  periodType=self.period_type,
                                                  frequencyType=self.frequency_type,
                                                  frequency=self.frequency,
                                                  end_date=self.end_date,
                                                  start_date=self.start_date)
        return self.get_content(price_endpoint)

    def get_fundamentals(self, ticker):
        fundamental_endpoint = config.fundamentals_url.format(stock_ticker=ticker,
                                                              projection=self.projection)
        return self.get_content(fundamental_endpoint)

    def get_options(self, ticker):
        options_endpoint = config.options_url.format(stock_ticker=ticker)
        return self.get_content(options_endpoint)

    def get_movers(self, index):
        movers_endpoint = config.movers_url.format(index=index,
                                                   direction=self.direction,
                                                   change=self.change)
        return self.get_content(movers_endpoint)

    def get_content(self, url):
        page = requests.get(url=url,
                            params={'apikey': self.api_key})
        return json.loads(page.content)


class TDDataPull:

    @staticmethod
    def pull_one_minute(ticker):
        tda = TDAmeritrade(period_type='day', frequency_type='minute')
        return tda.get_prices(ticker)

    @staticmethod
    def pull_five_minute(ticker):
        tda = TDAmeritrade(period_type='day', frequency_type='minute', frequency='5')
        return tda.get_prices(ticker)

    @staticmethod
    def pull_ten_minute(ticker):
        tda = TDAmeritrade(period_type='day', frequency_type='minute', frequency='10')
        return tda.get_prices(ticker)

    @staticmethod
    def pull_fifteen_minute(ticker):
        tda = TDAmeritrade(period_type='day', frequency_type='minute', frequency='15')
        return tda.get_prices(ticker)

    @staticmethod
    def pull_thirty_minute(ticker):
        tda = TDAmeritrade(period_type='day', frequency_type='minute', frequency='30')
        return tda.get_prices(ticker)

    @staticmethod
    def pull_hour(ticker):
        tda = TDAmeritrade(period_type='day', frequency_type='minute', frequency='60')
        return tda.get_prices(ticker)

    @staticmethod
    def pull_daily(ticker):
        tda = TDAmeritrade(period_type='year', frequency_type='daily', frequency='1')
        return tda.get_prices(ticker)

    @staticmethod
    def pull_weekly(ticker):
        tda = TDAmeritrade(period_type='year', frequency_type='weekly', frequency='1')
        return tda.get_prices(ticker)


if __name__ == "__main__":
    # tda = TDAmeritrade()
    # prices = tda.get_prices("TSLA")
    # options = tda.get_options("TSLA")
    # fund = tda.get_fundamentals("TSLA")
    # list_tickers = tda.get_all_tickers()
    tddp = TDDataPull()
    prices = tddp.pull_one_minute('TSLA')
    pass
