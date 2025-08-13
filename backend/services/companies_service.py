from database.connection import async_session
from models.Companies import Companies
from sqlalchemy.future import select

class CompaniesService:
    async def create_company(
        self, 
        name:str, 
        url_site:str, 
        url_linkedin:str, 
        url_instagram:str, 
        url_x:str
    ) -> Companies:
        
        async with async_session() as session:
            
            name = name.lower()
            
            company = Companies(
                name=name, 
                url_site=url_site, 
                url_linkedin=url_linkedin, 
                url_instagram=url_instagram, 
                url_x=url_x
            )
            
            session.add(company)
            await session.commit()
            await session.refresh(company)
                
        return company
    
    async def find_company(self, name:str = None) -> Companies:
        name = name.lower()
        
        async with async_session() as session:
            query = select(Companies).where(Companies.name == name)
            result  = await session.execute(query)
            
            company = result.scalars().one()
            
        return company
        
        