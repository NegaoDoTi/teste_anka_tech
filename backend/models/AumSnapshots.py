from database.base import Base
from sqlalchemy import Column, Integer, UUID, ForeignKey, VARCHAR
from sqlalchemy.dialects.postgresql import TEXT

class AumSnapshots(Base):
    __tablename__ = "aum_snapshots"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    scrape = Column(UUID, ForeignKey("scrape_logs.id"), nullable=False)
    aum = Column(TEXT, nullable=False)
    date = Column(VARCHAR(19), nullable=False)
    
    def __init__(self, scrape:str, aum:str, date:str) -> None:
        self.scrape = scrape
        self.aum = aum
        self.date = date