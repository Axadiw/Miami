from sqlalchemy import Column, String, DateTime, Numeric, Integer, BigInteger, ForeignKey

from models import Base


class SkippedGap(Base):
    __tablename__ = 'SkippedGaps'

    id = Column(Integer, primary_key=True)
    exchange = Column(Integer, ForeignKey('Exchanges.id'), nullable=False)
    symbol = Column(Integer, ForeignKey('Symbols.id'), nullable=False)
    timeframe = Column(Integer, ForeignKey('Timeframes.id'), nullable=False)
    start = Column(DateTime(), nullable=False)
    end = Column(DateTime(), nullable=False)

    def length(self):
        return self.end - self.start

    def __repr__(self):
        return f'SkippedGap {self.symbol.name} {self.timeframe.name} {self.start}\t-\t{self.end}\tlength: {self.length()}'
