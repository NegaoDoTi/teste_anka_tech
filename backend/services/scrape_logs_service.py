from database.connection import async_session
from models.ScrapeLogs import ScrapeLogs
from uuid import uuid4

class ScrapeLogsService:
    
    async def create_scrape_log(self, company_id:int, start:str) -> ScrapeLogs:
        async with async_session() as session:
            
            id = str(uuid4())
            
            scrape = ScrapeLogs(id=id, company=company_id, start=start)
            
            session.add(scrape)
            await session.commit()
            await session.refresh(scrape)
            
            await session.close()
        
        return scrape
    
    async def update_scrape_end(self, id:str, end:str) -> ScrapeLogs:
        async with async_session() as session:
            
            scrape = await session.get(ScrapeLogs, id)
            
            if not scrape:
                raise Exception(f"Scrape Log do id: {id} não encontrado no banco")
            
            scrape.end = end
            
            await session.commit()
            await session.refresh(scrape)
            
            await session.close()
            
        return scrape