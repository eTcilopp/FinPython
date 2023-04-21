from models import Database, SRCalculations, Tickers, PriceData
from  itertools import combinations 

import pandas as pd
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


    


def run(portfolio_size, sharpe_ratio_threshold):
    tickers = session.query(Tickers.ticker).join(SRCalculations).filter(SRCalculations.asr > sharpe_ratio_threshold).all()
    tickers = [ticker[0] for ticker in tickers]
    for i in get_combinations(tickers, portfolio_size):
        dataframe = get_dataframe(i)
        pass

if __name__ == '__main__':
    db = Database("sqlite:///stocks_data.db")
    session = db.session    
    portfolio_size = 4
    sharpe_ratio_threshold = 1.2
    run(portfolio_size, sharpe_ratio_threshold)