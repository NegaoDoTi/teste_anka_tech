from database.connection import async_session
from models.AumSnapshots import AumSnapshots

class AumSnapshotsService:
    
    async def create_aum_snapshot(self, scrape_id:str, aum:str, date:str) -> AumSnapshots:
        async with async_session() as session:
            
            aum_s = AumSnapshots(scrape=scrape_id, aum=aum, date=date)
            
            session.add(aum_s)
            await session.commit()
            await session.refresh(aum_s)
            
            await session.close()
            
        return aum_s