import yfinance as yf
from pyfinviz import Screener

def run():
    page = 3
    screener = Screener(pages=[x for x in range(1, page)])
    list_ticker = []
    for i in range(0, page):
        if i == 1:
            pass
        else:
            for j in range(len(screener.data_frames[i])):
                list_ticker.append(screener.data_frames[i].Ticker[j])
    print(list_ticker)


if __name__=='__main__':
    run()

