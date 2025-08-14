from queues.consume import RabbitConsume
from traceback import format_exc
from services.companies_service import CompaniesService
from services.scrape_logs_service import ScrapeLogsService
from services.aum_snapshots_service import AumSnapshotsService
from services.usage_service import UsageService
from datetime import datetime
from docling.document_converter import DocumentConverter
from scripts.extractors import extract_relevant_chunks
from scripts.agent import ChatGPTAgent
from services.dailycosta_service import DailyCostService
from scripts.generate_excel import generate_report
import asyncio
import logging

class StartScript():
    """Objeto que monta o robo de scraping
    """
    
    def __init__(self):
        self.company_service = CompaniesService()
        self.scrape_service = ScrapeLogsService()
        self.aum_service = AumSnapshotsService()
        self.usage_service = UsageService()
        self.dailycost_service = DailyCostService()
    
    
    def start(self) -> None:
        """Metodo responsavel por aplicar a logica e ordenar os scrips conforme seus resultados
        """
        
        try:
            
            export_list = []
            
            while True:
                consumer = RabbitConsume()
                
                consume_result = asyncio.run(consumer.consume_one())
                
                if consume_result == None:
                    break
                else:
                    consumer.channel.close()
                
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
                
                for key in consume_result:
                    if key == "name":
                        continue
                    
                    if consume_result[key] == "NÂO DISPONIVEL" or "NÂO DISPONIVEL" in consume_result[key]:
                        continue
                    
                    converter = DocumentConverter()
                    
                    converted_result = converter.convert(consume_result[key])
                    
                    text = converted_result.document.export_to_text()
                    
                    prompt = extract_relevant_chunks(text, company.name)
                    
                    now = datetime.now()
                    
                    now_date = now.date()
                    
                    dailycost = asyncio.run(self.dailycost_service.find_daily_cost(
                        day=now_date
                    ))
                    
                    if dailycost == None:
                        dailycost = asyncio.run(self.dailycost_service.create_daily_cost(
                            day=now_date
                        ))
                    
                    agent = ChatGPTAgent()
                    
                    usage = asyncio.run(self.usage_service.create_usage(
                        use=prompt["total_tokens"],
                        date=now_date.strftime("%d/%m/%Y"),
                        scrape_id=str(scrape.id)
                    ))
                    
                    response_agent = agent.ask_the_agent(prompt=prompt["prompt"], total_tokens=prompt["total_tokens"], now_day_cost=dailycost.cost)
                    
                    if "task_cost" in response_agent:
                        dailycost = asyncio.run(self.dailycost_service.upload_cost(
                            id=dailycost.id,
                            cost=dailycost.cost + response_agent["task_cost"]
                        ))
                    
                    now_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    
                    aum = asyncio.run(self.aum_service.create_aum_snapshot(
                        scrape_id=str(scrape.id),
                        aum=response_agent["message"],
                        date=now_string
                    ))
                    
                    export_list.append(
                        {
                            "company_name" : company.name,
                            "scrape_log" : str(scrape.id),
                            "scrape_start" : scrape.start,
                            "aum_id" : aum.id,
                            "aum" : aum.aum
                        }
                    )
                
                now = datetime.now()
                
                scrape = asyncio.run(self.scrape_service.update_scrape_end(
                    id=str(scrape.id),
                    end=now.strftime("%d/%m/%Y %H:%M:%S")
                ))
            
            report_result = generate_report(export_list)
            
            print(f"Scrape realizado com sucesso relatorio salvo no caminho: {report_result}")
            
            return
                
        except Exception:
            logging.error(format_exc())
            
            return