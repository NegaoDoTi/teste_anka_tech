from database.base import Base
from sqlalchemy import Column, Integer, VARCHAR, UUID, ForeignKey


class Usage(Base):
    __tablename__ = "usage"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    total_tokens = Column(Integer, nullable=False)
    date = Column(VARCHAR(10), nullable=False)
    scrape_id = Column(UUID, ForeignKey("scrape_logs.id"))
    
    def __init__(self, use:int, date:str, scrape_id:str) -> None:
        self.total_tokens = use
        self.date = date
        self.scrape_id = scrape_id