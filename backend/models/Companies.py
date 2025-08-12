from database.base import Base
from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship

class Companies(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(VARCHAR(255), index=True, unique=True)
    
    scrape_logs = relationship("ScrapeLogs", backref="ScrapeLogs", lazy=True)
    
    def __init__(self, name:str) -> None:
        self.name = name