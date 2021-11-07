from pydantic import BaseModel


class StockBase(BaseModel):
    id: int


class Stock(StockBase):
    symbol: str
    name: str

    class Config:
        orm_mode = True


class PriceBase(BaseModel):
    stock_id: int


class Price(PriceBase):
    id: int
    interval: str
    date_time: str
    open: float
    high: float
    low: float
    close: float
    volume: int

    class Config:
        orm_mode = True
