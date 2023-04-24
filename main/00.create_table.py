from sqlalchemy import create_engine
# from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Base, Tickers
from ticker import get_tickers
def run():
    engine = create_engine("sqlite:///stocks_data.db", echo=True)
    Base.metadata.create_all(engine)

if __name__=='__main__':
    run()