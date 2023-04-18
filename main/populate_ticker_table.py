from models import Database, Tickers
from ticker import get_tickers

def run(pages, session):
    def get_company(new_ticker):
        for ticker in fetched_data:
            if new_ticker == ticker[0]:
                return ticker[1]
    def get_industry(new_ticker):
        for ticker in fetched_data:
            if new_ticker == ticker[0]:
                return ticker[2]
        
    
    existing_tickers = [el[0] for el in session.query(Tickers.ticker).all()]
    fetched_data = get_tickers(pages)   # TODO: Make as variable
    fetched_tickers = [el[0] for el in fetched_data]
    
    new_tickers = list(set(fetched_tickers) - set(existing_tickers))
    
    new_objects = []
    for new_ticker in new_tickers:
        params = {
            'ticker': new_ticker,
            'company': get_company(new_ticker),
            'industry': get_industry(new_ticker)
        }
        new_objects.append(Tickers(**params))
    
    session.add_all(new_objects)
    session.commit()

if __name__=='__main__':
    pages = 300
    db = Database("sqlite:///stocks_data.db")
    session = db.session
    run(pages, session)