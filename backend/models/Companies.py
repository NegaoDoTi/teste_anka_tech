from database.base import Base
from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TEXT

class Companies(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(VARCHAR(255), index=True, unique=True)
    url_site = Column(TEXT)
    url_linkedin = Column(TEXT)
    url_instagram = Column(TEXT)
    url_x = Column(TEXT)
    
    scrape_logs = relationship("ScrapeLogs", backref="ScrapeLogs", lazy=True)
    
    def __init__(self, name:str) -> None:
        self.name = name