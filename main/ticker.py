import yfinance as yf
from pyfinviz import Screener
from datetime import datetime


def run():
    page = 30
    screener = Screener(pages=[x for x in range(1, page)])
    list_ticker = []
    for i in range(0, page):
        if i == 1:
            pass
        else:
            for j in range(len(screener.data_frames[i])):
                list_ticker.append(screener.data_frames[i].Ticker[j])


if __name__=='__name__':
    run()

