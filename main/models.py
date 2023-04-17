from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.schema import PrimaryKeyConstraint


class Database:
    def __init__(self, database_location: str, echo=False):
        self.engine = create_engine(database_location, echo=echo)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

class Base(DeclarativeBase):
    pass

class Tickers(Base):
    __tablename__ = 'tickers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(10), unique=True)
    
    def __repr__(self) -> str:
        return self.ticker

class PriceData(Base):
    __tablename__ = 'price_data'
    # __table_args__ = (
    #     PrimaryKeyConstraint('ticker_id', 'date'), {}
    # )

    # id: Mapped[int] = mapped_column(primary_key=True)
    ticker_id = Column(Integer, ForeignKey('tickers.id'), primary_key=True)
    date = Column(Date, primary_key=True)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Integer)
    