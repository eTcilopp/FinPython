from models import Database, SRCalculations, Tickers, PriceData
from  itertools import combinations 

import pandas as pd
import numpy as np
from functools import reduce

def get_combinations(lst, portfolio_size):
    # Get all possible combinations of the list in groups of four
    all_combinations = combinations(lst, portfolio_size)
    for combination in all_combinations:
        # Check if there are any duplicates in the current combination
        if len(set(combination)) == 4:
            yield list(combination)
            
def get_dataframe(ticker_lst):
    df_lst = []
    for ticker in ticker_lst:
        ticker_id = session.query(Tickers.id).where(Tickers.ticker==ticker).first()
        df = pd.read_sql(session.query(PriceData.date, PriceData.adj_close).where(PriceData.ticker_id==ticker_id[0]).statement, session.bind)
        df.set_index('date', inplace=True)
        df.rename(columns={'adj_close': ticker}, inplace=True)
        df_lst.append(df)
    
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['date'],how='outer'), df_lst)
    return df_merged

def get_portfolio_sharpe_rate(stocks, num_ports=5000):
    all_weights = np.zeros((num_ports, len(stocks.columns)))
    ret_arr = np.zeros(num_ports)
    vol_arr = np.zeros(num_ports)
    sharpe_arr = np.zeros(num_ports)
    
    log_ret = np.log(stocks/stocks.shift(1))
    
    for i in range(num_ports):
        weights = np.array(np.random.random(len(stocks.columns)))
        weights = weights/np.sum(weights)
        all_weights[i,:] = weights

        ret_arr[i] = np.sum((log_ret.mean() * weights) * 252)
        vol_arr[i] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))
        sharpe_arr[i] =  ret_arr[i] / vol_arr[i]

    max_sr = sharpe_arr.max()
    max_weights = all_weights[sharpe_arr.argmax()]
    max_sr_ret = ret_arr[sharpe_arr.argmax()]
    max_sr_vol = vol_arr[sharpe_arr.argmax()]
    
    return max_sr, max_weights


    


def run(portfolio_size, sharpe_ratio_threshold):
    tickers = session.query(Tickers.ticker).join(SRCalculations).filter(SRCalculations.asr > sharpe_ratio_threshold).all()
    tickers = [ticker[0] for ticker in tickers]
    for combination in get_combinations(tickers, portfolio_size):
        dataframe = get_dataframe(combination)
        portfolio_sr, portfolio_weights = get_portfolio_sharpe_rate(dataframe, num_ports=5000)
        print(f'Sharpe Ratio: {portfolio_sr}, weigts: {portfolio_weights}')
        pass

if __name__ == '__main__':
    db = Database("sqlite:///stocks_data.db")
    session = db.session    
    portfolio_size = 4
    sharpe_ratio_threshold = 1.2
    run(portfolio_size, sharpe_ratio_threshold)