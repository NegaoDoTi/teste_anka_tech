from database.base import Base
from sqlalchemy import Column, Integer, VARCHAR


class Usage(Base):
    __tablename__ = "usage"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    use = Column(Integer, nullable=False)
    date = Column(VARCHAR(10), nullable=False)
    
    def __init__(self, use:int, date:str) -> None:
        self.use = use
        self.date = date