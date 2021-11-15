import os

# CWD = os.getcwd()
# FRONTEND = CWD + "/frontend"
# BACKEND = CWD + "/backend"
# SCRIPTS = CWD + "/scripts"

HOST = 'localhost'
SQL_PASSWORD = 'password'
SQL_PORT = 5432
SQL_DB = 'test'
SQL_USER = 'jeremy'

tda_api_key = 'GGR3LEWNRQHMOKMVQPQFMIYFGGFIU8JG'
prices_url = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&' \
             'frequencyType={frequencyType}&frequency={frequency}&endDate={end_date}&startDate={start_date}'
fundamentals_url = 'https://api.tdameritrade.com/v1/instruments?&symbol={stock_ticker}&projection={projection}'
options_url = 'https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}'
# options_url = 'https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}&contractType={contract_type}' \
#               '&strikeCount={strike_count}&includeQuotes={include_quotes}&strategy={strategy}' \
#               '&strike={strike}&range={range}&fromDate={from_date}&toDate={to_date}&volatility={volatility}' \
#               '&underlyingPrice={underlying_price}&interestRate={interest_rate}&daysToExpiration={days_to_expire}' \
#               '&expMonth={exp_month}&optionType={option_type}'
movers_url = 'https://api.tdameritrade.com/v1/marketdata/{index}/movers&direction={direction}&change={change}'

ALPACA_ENDPOINT = 'https://paper-api.alpaca.markets'
ALPACA_API_KEY = 'PK9UUBO4AT5OM0GK9H1Q'
ALPACA_SECRET_KEY = 'yAj2fZNg5PusSIdjyGIHcI2FbZiwi1ZzbyCytfFq'

POLYGON_API_KEY = '13YHXchxQ2P0eymC0GMkbTarZeDD4vck'
POLYGON_ENDPOINT = f'https://api.polygon.io/v2/aggs/ticker/AAPL/' \
                   f'range/1/day/2020-06-01/2020-06-17?apiKey={POLYGON_API_KEY}'
