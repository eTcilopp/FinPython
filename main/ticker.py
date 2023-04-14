import yfinance as yf
from pyfinviz import Screener
import sqlalchemy as db



def run():
    page = 5
    screener = Screener(pages=[x for x in range(1, page)])
    ticker_lst = []
    for i in range(0, page):
        print(i)
        if i == 1:
            pass
        else:
            for j in range(len(screener.data_frames[i])):
                ticker_lst.append(screener.data_frames[i].Ticker[j])
    # print(ticker_lst)
    
    insertion_lst = [{'ticker': el} for el in ticker_lst]
    print(insertion_lst)
    
    # path_to_file = r'\\server\path\to\file\stocks_data.db'
    # engine = db.create_engine(f'sqlite:///{path_to_file}')
    
    engine = db.create_engine('sqlite:///stocks_data.db')
    connection = engine.connect()
    metadata = db.MetaData()
    
    tickers = db.Table('tickers', metadata,
        db.Column('ticker_id', db.Integer, autoincrement=True, primary_key=True),
        db.Column('ticker', db.Text, unique=True)
        )
    
    metadata.create_all(engine)
    
    # insertion_query = tickers.insert().values([
    #     {'ticker': 'MSFT'}
    # ])
    
    new_ticker_insertion_list = []
    for ticker in insertion_lst:
        # print(ticker['ticker'])
        # select_ticket_query = db.select([tickers]).where(tickers.columns.ticker==ticker['ticker'])
        select_ticket_query = tickers.select().where(tickers.columns.ticker==ticker['ticker'])
        res = connection.execute(select_ticket_query)
        print(res.fetchall())
        if len(res.fetchall())==0:
            new_ticker_insertion_list.append(ticker)
            print(ticker)


            
    print(f'>>>> {len(new_ticker_insertion_list)}')
    
    insertion_query = tickers.insert().values(new_ticker_insertion_list)
    # insertion_query_sql = insertion_query.on_conflict_do_nothing(index_elements=['ticker'])
    
    # connection.execute(tickers.insert(), insertion_lst)
    connection.execute(insertion_query)
    
    connection.commit()
    
    

if __name__=='__main__':
    run()
    print('all done')

