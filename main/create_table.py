from sqlalchemy import create_engine
# from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Base, Tickers
from ticker import get_tickers
def run():
    engine = create_engine("sqlite:///stocks_data.db", echo=True)
    Base.metadata.create_all(engine)

    # session = Session(engine)
    # existing_tickers = [el[0] for el in session.query(Tickers.ticker).all()]
    # fetched_tickers = get_tickers(100)
    
    # new_tickers = list(set(fetched_tickers) - set(existing_tickers))
    
    # new_objects = []
    # for new_ticker in new_tickers:
    #     new_objects.append(Tickers(ticker=new_ticker))
    
    # session.add_all(new_objects)
    # session.commit()


if __name__=='__main__':
    run()