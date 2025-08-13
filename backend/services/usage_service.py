from database.connection import async_session
from models.Usage import Usage

class UsageService:
    
    async def create_usage(self, use:int, date:str) -> Usage:
        async with async_session() as session:
            usage = Usage(use=use, date=date)
            
            session.add(usage)
            
            await session.commit()
            await session.refresh(usage)
            
        return usage