import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from models import Database, Tickers, PriceData

def write_to_database(session, data, ticker_id):
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

def get_ticker_id(session, ticker_name):
    ticker = session.query(Tickers).filter(Tickers.ticker==ticker_name).first()
    if ticker is not None:
        return ticker.id
    else:
        try:
            yf.Ticker(ticker_name).info
            new_ticker = Tickers(ticker=ticker_name)
            session.add(new_ticker)
            session.commit()
            return new_ticker.id
        except Exception:
            return

def run(ticker_name: str, start_date: str, end_date: str, write_to_db=False):
    # initial_investment = 100000

    db = Database("sqlite:///stocks_data.db")
    session = db.session
    
    ticker_id = get_ticker_id(session, ticker_name)
    if not ticker_id:
        print(f'{ticker_name} not found')
        return

    yf.pdr_override()
    data = pdr.get_data_yahoo(ticker_name, start=start_date, end=end_date)

    if write_to_db:
        write_to_database(session, data, ticker_id)
    
    return data

if __name__=='__main__':
    start_date = '2020-03-01'
    end_date = '2022-03-01'
    run('TSLA', start_date, end_date, write_to_db=True)
    print('All done!')
