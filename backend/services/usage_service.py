from database.connection import async_session
from models.Usage import Usage
from sqlalchemy.future import select

class UsageService:
    
    async def create_usage(self, use:int, date:str, scrape_id:str) -> Usage:
        async with async_session() as session:
            usage = Usage(use=use, date=date, scrape_id=scrape_id)
            
            session.add(usage)
            
            await session.commit()
            await session.refresh(usage)
            
            await session.close()
            
        return usage
    
    async def find_all(self, date:str) -> list[Usage]:
        async with async_session() as session:
            query = select(Usage).where(Usage.date == date)
            
            response = await session.execute(query)
            try:
                results = response.scalars().all()
            except:
                results = []
            
            await session.close()
        
        usages = []
        
        for result in results:
                usages.append(result)
                
        return usages
            
            