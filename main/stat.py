import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Tickers, PriceData


def run(ticker_name: str):
    start = '2020-03-01'
    end = '2022-03-01'
    initial_investment = 100000
    yf.pdr_override()
    data = pdr.get_data_yahoo(ticker_name, start="2021-04-01", end="2023-04-01")
    # data.reset_index()
    # ticker = yf.Ticker(ticker_name)
    # hist = ticker.history(period="2y")
    engine = create_engine("sqlite:///stocks_data.db", echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    ticker = session.query(Tickers).filter(Tickers.ticker==ticker_name).first()
    if ticker is not None:
        ticker_id = ticker.id
    else:
        # TODO: Add to the database
        pass
    # data['ticker_id'] = ticker_id
    # data.set_index('Date')
    new_objects = []
    for _, row in data.reset_index().iterrows():
        existing_record = session.query(PriceData).filter(PriceData.ticker_id==ticker_id, PriceData.date==row['Date']).first()
        if existing_record is not None:
            if existing_record.adj_close == row['Adj Close']:
                continue
            existing_record.delete()
            session.commit()
            
        params = {
            'ticker_id': ticker_id,
            'date': row['Date'],
            'open': row['Open'],
            'high': row['High'],
            'low': row['Low'],
            'close': row['Close'],
            'adj_close': row['Adj Close'],
            'volume': row['Volume']
        }
        new_objects.append(PriceData(**params))
    session.add_all(new_objects)
    session.commit()
        
        # pass
    # data.reset_index().to_sql('price_data', engine, if_exists='replace', index=False)
    # TODO: Why do you need override here? Verify..
    # TODO: Move database stuff to another module
    
    

if __name__=='__main__':
    run('ADBE')
    print('All done!')