import pandas as pd
import numpy as np
from pandas_datareader import data as pdr
import yfinance as yf
from models import Database, Tickers, PriceData, SRCalculations
from datetime import datetime

def get_sharpe_ratio(data):
    stocks = data['Adj Close']
    log_ret = np.log(stocks/stocks.shift(1))
    expected_return = log_ret.mean()
    expected_volatility = log_ret.std()
    sr = expected_return/expected_volatility
    asr = (252**0.5) * sr
    return asr
    

def write_to_database(session, data, ticker_id):
    new_objects = []
    for _, row in data.reset_index().iterrows():
        existing_record = session.query(PriceData).filter(PriceData.ticker_id==ticker_id, PriceData.date==row['Date']).first()
        if existing_record is not None:
            if existing_record.adj_close == row['Adj Close']:
                continue
            session.delete(existing_record)
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

def get_ticker_obj(session, ticker_name):
    try:
        yf.Ticker(ticker_name).info
        new_ticker = Tickers(ticker=ticker_name)
        session.add(new_ticker)
        session.commit()
        return new_ticker
    except Exception:
        return

def run(session, ticker, start_date: str, end_date: str, write_to_db=False):
    # initial_investment = 100000
    
    # ticker_id = get_ticker_id(session, ticker_name)
    # if not ticker_id:
    #     print(f'{ticker.ticker} not found')
    #     return

    yf.pdr_override()
    data = pdr.get_data_yahoo(ticker.ticker, start=start_date, end=end_date)

    if write_to_db:
        write_to_database(session, data, ticker.id)
    
    return data

# TODO; If failed to download - delete it nahren
# TODO: add company name - impossible to find by ticker only
# TODO: ATT CAPITALIZATION AND OTHER PARAMS FROM SCREENING
# TODO: ADD USAGE OF SAVED DATA

if __name__=='__main__':
    asr_threshold = 0.9
    start_date = '2020-03-01'
    end_date = '2023-03-01'
    
    db = Database("sqlite:///stocks_data.db")
    session = db.session
    
    tickers = session.query(Tickers).all()
    # tickers = tickers[:300]  # TODO: Remove me
    
    for ticker_obj in tickers:
        data = run(session, ticker_obj, start_date, end_date, write_to_db=True)
        asr = get_sharpe_ratio(data)
        # print(asr)
        if asr < asr_threshold:
            continue
        params = {
            'ticker_id': ticker_obj.id,
            'calc_date': datetime.now(),
            'data_start_date': datetime.strptime(start_date, '%Y-%m-%d'),
            'data_end_date': datetime.strptime(end_date, '%Y-%m-%d'),
            'asr': asr  
        }

        # existing_value=session.query(SRCalculations).filter(*params)
        session.add(SRCalculations(**params))
        session.commit()
        print(f'ASR for {ticker_obj.ticker}: {asr}')
        
    
    
    
    # ticker_obj = session.query(Tickers).filter(Tickers.ticker==ticker_str).first()
    # if ticker_obj is None:
    #     ticker_obj = get_ticker_obj(session, ticker_str)
    # if ticker_obj is None:
    #     print('ticker cannot be found')
    #     # TODO: break

    
    # data = run(session, ticker_obj, start_date, end_date, write_to_db=True)
    # asr = get_sharpe_ratio(data)
    
    # params = {
    #     'ticker_id': ticker_obj.id,
    #     'calc_date': datetime.now(),
    #     'data_start_date': datetime.strptime(start_date, '%Y-%m-%d'),
    #     'data_end_date': datetime.strptime(end_date, '%Y-%m-%d'),
    #     'asr': asr  
    # }
    # session.add(SRCalculations(**params))
    # session.commit()
    
    # print(f'ASR: {asr}')
    print('All done!')
