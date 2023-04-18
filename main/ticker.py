import yfinance as yf
from pyfinviz import Screener

def get_filtered_dataframe(dataframe):
    dataframe = dataframe[(dataframe.Country=='USA') & (dataframe.MarketCap.str.contains('B'))]
    return dataframe

def get_tickers(to_page):
    screener = Screener(pages=[x for x in range(1, to_page)])
    ticker_lst = []
    for i in range(0, to_page):
        dataframe = screener.data_frames[i]
        if dataframe is not None:
            dataframe = get_filtered_dataframe(dataframe)
            ticker_lst += dataframe[['Ticker', 'Company']].values.tolist()
    return ticker_lst

if __name__=='__main__':
    to_page = 3
    ticker_lst = get_tickers(to_page)
    print(ticker_lst)
    print('all done')

