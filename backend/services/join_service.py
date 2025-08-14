from sqlalchemy import select, desc
from models.ScrapeLogs import ScrapeLogs
from models.Companies import Companies
from database.connection import async_session

class JoinsService:
    
    async def join_company_scrapelogs(self) -> list[Companies]:
        async with async_session() as session:
            latest_logs_subquery = select(ScrapeLogs).order_by(desc(ScrapeLogs.start)).limit(5).subquery("latest_logs")
            
            query = select(Companies).join(
                latest_logs_subquery,
                Companies.id == latest_logs_subquery.c.company
            )

            response = await session.execute(query)
            try:
                result = response.scalars().all()
            except:
                result = []
                
            await session.close()
            
        return result
                     
    