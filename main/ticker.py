import yfinance as yf
from pyfinviz import Screener


def get_tickers(to_page):

    screener = Screener(pages=[x for x in range(1, to_page)])
    ticker_lst = []
    for i in range(0, to_page):
        dataframe = screener.data_frames[i]
        if dataframe is not None:
            for j in range(len(dataframe)):
                ticker_lst.append(dataframe.Ticker[j])
    return ticker_lst

if __name__=='__main__':
    page = 5
    get_tickers(page)
    print('all done')

