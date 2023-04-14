from sqlalchemy import create_engine
from models import Base
def run():
    engine = create_engine("sqlite:///stocks_data.db", echo=True)
    Base.metadata.create_all(engine)

if __name__=='__main__':
    run()