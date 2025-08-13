from queues.consume import RabbitConsume
from traceback import format_exc
from services.companies_service import CompaniesService
from services.scrape_logs_service import ScrapeLogsService
from services.aum_snapshots_service import AumSnapshotsService
from services.usage_service import UsageService
from datetime import datetime
import asyncio

class StartScript():
    
    def __init__(self):
        self.company_service = CompaniesService()
        self.scrape_service = ScrapeLogsService()
        self.aum_service = AumSnapshotsService()
        self.usage_service = UsageService()
    
    
    def start(self) -> None:
        try:
            
            while True:
                consumer = RabbitConsume()
                
                consume_result = asyncio.run(consumer.consume_one())
                
                if consume_result == None:
                    break
                
                company = asyncio.run(self.company_service.find_company(name=consume_result["name"]))
                
                if company == None:
                
                    company = asyncio.run(self.company_service.create_company(
                        name=consume_result["name"],
                        url_site=consume_result["url_site"],
                        url_linkedin=consume_result["url_linkedin"],
                        url_instagram=consume_result["url_instagram"],
                        url_x=consume_result["url_x"]
                    ))
                else:
                    company = asyncio.run(self.company_service.update_company(
                        id=company.id,
                        name=consume_result["name"],
                        url_site=consume_result["url_site"],
                        url_linkedin=consume_result["url_linkedin"],
                        url_instagram=consume_result["url_instagram"],
                        url_x=consume_result["url_x"]
                    ))
                    
                now = datetime.now()
                
                scrape = asyncio.run(self.scrape_service.create_scrape_log(
                    company_id=company.id,
                    start=now.strftime("%d/%m/%Y %H:%M:%S")
                ))
            
        except Exception:
            print(format_exc())