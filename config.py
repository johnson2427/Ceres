import os

# CWD = os.getcwd()
# FRONTEND = CWD + "/frontend"
# BACKEND = CWD + "/backend"
# SCRIPTS = CWD + "/scripts"

HOST = 'localhost'
SQL_PASSWORD = 'password'
SQL_PORT = 5432
SQL_DB = 'test'
SQL_USER = 'postgres'

tda_api_key = 'GGR3LEWNRQHMOKMVQPQFMIYFGGFIU8JG'
prices_url = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&' \
             'period={period}&frequencyType={frequencyType}&frequency={frequency}'
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