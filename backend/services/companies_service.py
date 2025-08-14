from database.connection import async_session
from models.Companies import Companies
from sqlalchemy.future import select
import asyncio

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
            
            await session.close()
                
        return company
    
    async def find_company(self, name:str = None) -> Companies | None:
        name = name.lower()
        
        async with async_session() as session:
            query = select(Companies).where(Companies.name == name)
            result  = await session.execute(query)
            try:
                company = result.scalars().one()
            except:
                company = None
            
            await session.close()
            
        return company
    
    async def update_company(
        self,
        id:int,
        name:str = None, 
        url_site:str = None, 
        url_linkedin:str = None, 
        url_instagram:str = None, 
        url_x:str = None
    ) -> Companies:
        
        async with async_session() as session:
            company = await session.get(Companies, id)
            
            name = name.lower()
            
            if name:
                company.name = name
            
            if url_site:
                company.url_site = url_site
            
            if url_linkedin:
                company.url_linkedin = url_linkedin
            
            if url_instagram:
                company.url_instagram = url_instagram

            if url_x:
                company.url_x = url_x
                
            await session.commit()
            await session.refresh(company)
            
            await session.close()
            
        return company