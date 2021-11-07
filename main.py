from fastapi import FastAPI, Request, Depends, BackgroundTasks, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from models import StockFundamentals, Stocks, StockPrices


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def home(request: Request, forward_pe=None, dividend_amount=None, ma50=None, ma200=None, db: Session = Depends(get_db)):
    stock_filter = request.query_params.get('filter', False)
    stocks = db.query(Stocks)
    # if forward_pe:
    #     stocks = stocks.filter(StockFundamentals.forward_pe < forward_pe)
    # if dividend_amount:
    #     stocks = stocks.filter(StockFundamentals.dividendAmount > dividend_amount)
    # if ma50:
    #     stocks = stocks.filter(StockFundamentals.price > StockFundamentals.ma50)
    # if ma200:
    #     stocks = stocks.filter(StockFundamentals.price > StockFundamentals.ma200)
    prices = db.query(StockPrices).filter(StockPrices.high)
    if stock_filter == 'new_intraday_highs':
        pass
    if stock_filter == 'new_closing_highs':
        pass
    if stock_filter == 'new_intraday_lows':
        pass
    if stock_filter == 'new_closing_lows':
        pass
    stocks = stocks.order_by(Stocks.symbol)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "stocks": stocks,
        "dividend_yield": dividend_amount,
        "forward_pe": forward_pe,
        "ma200": ma200,
        "ma50": ma50
    })


@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol, db: Session = Depends(get_db)):
    stock = db.query(Stocks)
    stock = stock.filter(Stocks.symbol == symbol).first()
    stock_id = stock.id
    prices = db.query(StockPrices)
    prices = prices.filter(StockPrices.stock_id == stock_id)
    strategies = db.query(models.Strategy).all()
    return templates.TemplateResponse("stock_detail.html", {
        "request": request,
        "ticker": symbol,
        "stock": stock,
        "prices": prices,
        "strategies": strategies
    })


@app.post("/apply_strategy")
def apply_strategy(strategy_id: int = Form(...), stock_id: int = Form(...), db: Session = Depends(get_db)):
    stock_strategy = models.StockStrategy(strategy_id=strategy_id, stock_id=stock_id)
    db.add(stock_strategy)
    db.commit()
    db.refresh(stock_strategy)
    return RedirectResponse(url=f"/strategy/{strategy_id}", status_code=303)


@app.get("/strategy/{strategy_id}")
def strategy(request: Request, strategy_id, db: Session = Depends(get_db)):
    strategy = db.query(models.Strategy)
    strategy = strategy.filter(models.Strategy.id == strategy_id).first()
    stocks = db.query(models.StockStrategy).filter(models.StockStrategy.strategy_id == strategy_id).all()
    stock_ids = []
    for stock in stocks:
        stock_ids.append(stock.stock_id)
    app_strat_stocks = db.query(Stocks).filter(Stocks.id.in_(stock_ids)).all()
    return templates.TemplateResponse("strategy.html", {
        "request": request,
        "strategy": strategy,
        "stocks": app_strat_stocks
    })


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
