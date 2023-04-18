from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.sql import func


class Database:
    def __init__(self, database_location: str, echo=False):
        self.engine = create_engine(database_location, echo=echo)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

class Base(DeclarativeBase):
    pass

class Tickers(Base):
    __tablename__ = 'tickers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String)
    company = Column(String)
    industry = Column(String)
    
    def __repr__(self) -> str:
        return self.ticker

class PriceData(Base):
    __tablename__ = 'price_data'
    ticker_id = Column(Integer, ForeignKey('tickers.id'), primary_key=True)
    date = Column(Date, primary_key=True)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Integer)

class SRCalculations(Base):
    __tablename__ = 'sharpe_ratio_calc'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker_id = Column(Integer, ForeignKey('tickers.id'))
    calc_date = Column(DateTime(timezone=True), server_default=func.now())
    data_start_date = Column(Date)
    data_end_date = Column(Date)
    asr = Column(Float)
    
    