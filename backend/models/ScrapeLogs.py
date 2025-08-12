from database.base import Base
from sqlalchemy import Integer, UUID, VARCHAR, Column, ForeignKey
from sqlalchemy.orm import relationship

class ScrapeLogs(Base):
    __tablename__ = "scrape_logs"
    id = Column(UUID, primary_key=True, index=True)
    company = Column(Integer, ForeignKey("companies.id"), nullable=False)
    start = Column(VARCHAR(19), nullable=True)
    end = Column(VARCHAR(19))
    
    aum = relationship("AumSnapshots", backref="AumSnapshots", lazy=False)
    
    def __init__(self, id:str, company:int, start:str) -> None:
        self.id = id
        self.company = company
        self.start = start