from database.connection import async_session
from models.Usage import Usage

class UsageService:
    
    async def create_usage(self, use:int, date:str, scrape_id:str) -> Usage:
        async with async_session() as session:
            usage = Usage(use=use, date=date, scrape_id=scrape_id)
            
            session.add(usage)
            
            await session.commit()
            await session.refresh(usage)
            
        return usage