from services.usage_service import UsageService
from services.join_service import JoinsService
from queues.publish import RabbitPublish
from datetime import datetime

class UsageController:
    """Controller da rota usage/today
    """
    
    def __init__(self):
        self.usage_service = UsageService()
        self.join_service = JoinsService()
        
    async def get_all_usage_today(self) -> list:
        """Pega todos o usage do dia atual

        Returns:
            list: lita com informações do usages do dia atual
        """
        
        
        now = datetime.now().strftime("%d/%m/%Y")
        
        usages = await self.usage_service.find_all(date=now)
        
        datas = []
        
        for usage in usages:
            datas.append(
                {
                    "id" : usage.id,
                    "total_tokens" : usage.total_tokens,
                    "date" : usage.date,
                    "scrape_id" : str(usage.scrape_id)
                }
            )
        
        return datas
    
    async def rescrape_last_companies_today(self) -> bool:
        """Responsavel por aplicar a logica que reenvia a 5 ultimas cidade do dia atual para fila novamente

        Returns:
            bool: Se for true sucesso ao reenviar se nao false
        """
        
        result = await self.join_service.join_company_scrapelogs()
        
        if len(result) == 0:
            return False
            
        publish = RabbitPublish()
        
        for company in result:
            data =  {
                "name" : company.name,
                "url_site" : company.url_site,
                "url_linkedin" : company.url_linkedin,
                "url_instagram" : company.url_instagram,
                "url_x" : company.url_x
            }
            
            await publish.publish_one(data)  
            
        publish.channel.close()
        
        return True

            
            