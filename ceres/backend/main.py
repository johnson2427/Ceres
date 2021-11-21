import os

from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ceres.backend.db.database import SessionLocal, engine
from ceres.backend.models import models
from ceres.backend.models.models import Stocks, StockPrices
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="../templates")
print(os.getcwd() + "/ceres/templates/")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    stock_filter = request.query_params.get('filter', False)
    stocks = db.query(Stocks)
    if stock_filter == 'new_closing_highs':
        pass
    elif stock_filter == 'new_closing_lows':
        pass
    elif stock_filter == 'rsi_overbought':
        pass
    elif stock_filter == 'rsi_oversold':
        pass
    stocks = stocks.order_by(Stocks.symbol)
    # return templates.TemplateResponse("home.html", {
    #     "request": request,
    #     "stocks": stocks,
    # })
    json_encoded_stocks = jsonable_encoder(stocks.all())

    return JSONResponse(content=json_encoded_stocks)


@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol, db: Session = Depends(get_db)):
    stock = db.query(Stocks)
    stock = stock.filter(Stocks.symbol == symbol).first()
    stock_id = stock.id
    prices = db.query(StockPrices)
    prices = prices.filter(StockPrices.stock_id == stock_id)

    # need to extract the data from the queries and encode them into dictionaries
    json_encoded_prices = jsonable_encoder(prices.all())
    json_encoded_strategies = jsonable_encoder(db.query(models.Strategy).all())

    return JSONResponse(content={
        "symbol": symbol,
        "prices": json_encoded_prices,
        "strategies": json_encoded_strategies
    })


@app.post("/apply_strategy")
def apply_strategy(strategy_id: int = Form(...), stock_id: int = Form(...), db: Session = Depends(get_db)):
    stock_strategy = models.StockStrategy(strategy_id=strategy_id, stock_id=stock_id)
    db.add(stock_strategy)
    db.commit()
    db.refresh(stock_strategy)
    return RedirectResponse(url=f"/strategy/{strategy_id}", status_code=303)


@app.get("/strategies")
def strategies(request: Request, db: Session = Depends(get_db)):
    stock_strategies = db.query(models.Strategy).all()
    return templates.TemplateResponse("strategies.html", {
        "request": request,
        "strategies": stock_strategies
    })


@app.get("/orders")
def strategies(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("orders.html", {
        "request": request,
    })


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

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
