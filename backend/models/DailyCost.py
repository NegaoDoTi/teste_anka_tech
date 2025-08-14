from sqlalchemy import Column, Integer, VARCHAR, Float, DATE
from datetime import datetime
from database.base import Base

class DailyCost(Base):
    __tablename__ = "dailycost"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    cost = Column(Float, nullable=False)
    day = Column(DATE(), nullable=False, unique=True)
    
    def __init__(self, day:datetime, cost:float = 0 ) -> None:
        self.cost = cost
        self.day = day