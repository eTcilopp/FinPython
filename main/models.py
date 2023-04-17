from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker_id = Column(Integer, ForeignKey('tickers.id'))
    date = Column(Date)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Integer)
    