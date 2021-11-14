from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean, ARRAY
from ceres.backend.db.database import Base


class Stocks(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)


class StockFundamentals(Base):
    __tablename__ = "fundamentals"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    price = Column(Numeric(10, 2))
    forward_pe = Column(Numeric(10, 2))
    forward_eps = Column(Numeric(10, 2))
    ebitdaMargins = Column(Numeric(10, 6))
    profitMargins = Column(Numeric(10, 6))
    grossMargins = Column(Numeric(10, 6))
    operatingCashflow = Column(Numeric(15, 0))
    revenueGrowth = Column(Numeric(10, 6))
    operatingMargins = Column(Numeric(10, 6))
    ebitda = Column(Numeric(15, 0))
    targetLowPrice = Column(Numeric(10, 2))
    recommendationKey = Column(String)
    grossProfits = Column(Numeric(15, 0))
    freeCashflow = Column(Numeric(15, 0))
    targetMedianPrice = Column(Numeric(10, 2))
    earningsGrowth = Column(Numeric(10, 4))
    numberOfAnalystOpinions = Column(Integer)
    targetMeanPrice = Column(Numeric(10, 2))
    debtToEquity = Column(Numeric(10, 2))
    targetHighPrice = Column(Numeric(10, 2))
    totalCash = Column(Numeric(15, 0))
    totalDebt = Column(Numeric(15, 0))
    totalRevenue = Column(Numeric(15, 0))
    totalCashPerShare = Column(Numeric(10, 2))
    revenuePerShare = Column(Numeric(10, 2))
    bookValue = Column(Numeric(10, 2))
    sharesShort = Column(Numeric(15, 0))
    sharesPercentSharesOut = Column(Numeric(10, 6))
    heldPercentInstitutions = Column(Numeric(10, 4))
    heldPercentInsiders = Column(Numeric(10, 4))
    shortRatio = Column(Numeric(10, 4))
    sharesShortPreviousMonthDate = Column(Numeric(15, 0))
    floatShares = Column(Numeric(15, 0))
    ma50 = Column(Numeric(10, 2))
    ma200 = Column(Numeric(10, 2))
    high52 = Column(Numeric(10, 2))
    low52 = Column(Numeric(10, 2))
    dividendAmount = Column(Numeric(10, 2))
    dividendYield = Column(Numeric(10, 2))
    dividendDate = Column(DateTime)
    peRatio = Column(Numeric(10, 2))
    pegRatio = Column(Numeric(10, 2))
    pbRatio = Column(Numeric(10, 2))
    prRatio = Column(Numeric(10, 2))
    pcfRatio = Column(Numeric(10, 2))
    grossMarginTTM = Column(Numeric(10, 2))
    grossMarginMRQ = Column(Numeric(10, 2))
    netProfitMarginTTM =Column(Numeric(10, 2))
    netProfitMarginMRQ = Column(Numeric(10, 2))
    operatingMarginTTM = Column(Numeric(10, 2))
    operatingMarginMRQ = Column(Numeric(10, 2))
    returnOnEquity = Column(Numeric(10, 2))
    returnOnAssets = Column(Numeric(10, 2))
    returnOnInvestment = Column(Numeric(10, 2))
    quickRatio = Column(Numeric(10, 2))
    currentRatio = Column(Numeric(10, 2))
    interestCoverage = Column(Numeric(10, 2))
    totalDebtToCapital = Column(Numeric(10, 2))
    ltDebtToEquity = Column(Numeric(10, 2))
    totalDebtToEquity = Column(Numeric(10, 2))
    epsTTM = Column(Numeric(10, 2))
    epsChangePercentTTM = Column(Numeric(10, 2))
    epsChangeYear = Column(Numeric(10, 2))
    epsChange = Column(Numeric(10, 2))
    revChangeYear = Column(Numeric(10, 2))
    revChangeTTM = Column(Numeric(10, 2))
    revChangeIn = Column(Numeric(10, 2))
    sharesOutstanding = Column(Numeric(15, 2))
    marketCapFloat = Column(Numeric(10, 2))
    marketCap = Column(Numeric(10, 2))
    bookValuePerShare = Column(Numeric(10, 2))
    shortIntToFloat = Column(Numeric(10, 2))
    shortIntDayToCover = Column(Numeric(10, 2))
    divGrowthRate3Year = Column(Numeric(10, 2))
    beta = Column(Numeric(10, 4))
    vol1DayAvg = Column(Numeric(12, 0))
    vol10DayAvg = Column(Numeric(12, 0))
    vol3MonthAvg = Column(Numeric(12, 0))


class StockPrices(Base):
    __tablename__ = "prices_new"

    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    interval = Column(String)
    datetime = Column(DateTime)
    open = Column(Numeric(10, 2))
    high = Column(Numeric(10, 2))
    low = Column(Numeric(10, 2))
    close = Column(Numeric(10, 2))
    volume = Column(Integer)
    sma20 = Column(Numeric(10, 2))
    sma50 = Column(Numeric(10, 2))
    sma100 = Column(Numeric(10, 2))
    sma200 = Column(Numeric(10, 2))
    bb_lower = Column(Numeric(10, 2))
    bb_middle = Column(Numeric(10, 2))
    bb_upper = Column(Numeric(10, 2))
    macd = Column(Numeric(10, 2))
    macd_signal = Column(Numeric(10, 2))
    macd_histogram = Column(Numeric(10, 2))
    rsi14 = Column(Numeric(10, 2))


class StockOptions(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    strategy = Column(Integer)
    interval = Column(Numeric(10, 2))
    isDelayed = Column(Boolean)
    isIndex = Column(Boolean)
    interestRate = Column(Numeric(10, 2))
    underlyingPrice = Column(Numeric(10, 2))
    volatility = Column(Numeric(10, 2))
    daysToExpiration = Column(Numeric(10, 2))
    numberOfContracts = Column(Integer)
    callExpDateMap = Column(ARRAY(String))
    putExpDateMap = Column(ARRAY(String))


class Strategy(Base):
    __tablename__ = "strategy"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class StockStrategy(Base):
    __tablename__ = "stock_strategy"

    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    strategy_id = Column(Integer, ForeignKey("strategy.id"))
