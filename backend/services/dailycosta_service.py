from datetime import datetime
from models.DailyCost import DailyCost
from database.connection import async_session
from sqlalchemy.future import select


class DailyCostService:
    async def create_daily_cost(self, day:datetime, cost:float = 0.0) -> DailyCost:
        async with async_session() as session:
            dailycost = DailyCost(day=day, cost=cost)
            
            session.add(dailycost)
            
            await session.commit()
            await session.refresh(dailycost)
            
            await session.close()
            
        return dailycost
    
    async def find_daily_cost(self, day:datetime) -> DailyCost | None:
        async with async_session() as session:
            query = select(DailyCost).where(DailyCost.day == day)
            result  = await session.execute(query)
            
            try:
                dailycost = result.scalars().one()
            except:
                dailycost = None
            
            await session.close()
            
        return dailycost
    
    async def upload_cost(self, id:int, cost:float) -> DailyCost:
        async with async_session() as session:
            dailycost = await session.get(DailyCost, id)
            
            if cost:
                dailycost.cost = cost
                
            await session.commit()
            await session.refresh(dailycost)
            
            await session.close()
            
        return dailycost