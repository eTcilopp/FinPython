import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Tickers


def run(ticker_name: str):
    start = '2020-03-01'
    end = '2022-03-01'
    initial_investment = 100000
    yf.pdr_override()
    data = pdr.get_data_yahoo(ticker_name, start="2021-04-01", end="2023-04-01")
    # data.reset_index()
    # ticker = yf.Ticker(ticker_name)
    # hist = ticker.history(period="2y")
    engine = create_engine("sqlite:///stocks_data.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    ticker = session.query(Tickers).filter(Tickers.ticker==ticker_name).first()
    if ticker is not None:
        ticker_id = ticker.id
    else:
        # TODO: Add to the database
        pass
    data['ticker_id'] = ticker_id
    data.reset_index().to_sql('price_data', engine, if_exists='replace', index=False)
    
    

if __name__=='__main__':
    run('MSFT')
    print('All done!')