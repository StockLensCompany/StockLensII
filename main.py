from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_price(info: dict):
    return (
        info.get("currentPrice") or
        info.get("regularMarketPrice") or
        info.get("navPrice") or
        info.get("previousClose") or
        info.get("regularMarketPreviousClose")
    )

@app.get("/stock/{ticker}")
def get_stock(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "ticker": ticker,
        "name": info.get("shortName"),
        "price": get_price(info),
        "change_percent": info.get("regularMarketChangePercent"),
        "market_cap": info.get("marketCap"),
        "currency": info.get("currency"),
        "exchange": info.get("exchange"),
    }

@app.get("/etf/{ticker}")
def get_etf(ticker: str):
    etf = yf.Ticker(ticker)
    info = etf.info

    return {
        "ticker": ticker,
        "name": info.get("shortName"),
        "price": get_price(info),
        "change_percent": info.get("regularMarketChangePercent"),
        "currency": info.get("currency"),
        "exchange": info.get("exchange"),
        "total_assets": info.get("totalAssets"),
        "expense_ratio": info.get("annualReportExpenseRatio"),
        "ytd_return": info.get("ytdReturn"),
        "category": info.get("category"),
        "fund_family": info.get("fundFamily"),
    }

@app.get("/history/{ticker}")
def get_history(ticker: str, period: str = "1mo"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist["Close"].dropna().to_dict()
