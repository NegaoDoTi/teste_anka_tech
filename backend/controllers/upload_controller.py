from pathlib import Path
from uuid import uuid4
from csv import DictReader
from queues.publish import RabbitPublish

class UploadController:
    """Controller da rota Upload
    """
    
    def __init__(self):
        self.upload_path = Path(Path(__file__).parent.parent, "uploads")
        
        if not self.upload_path.exists():
            self.upload_path.mkdir()
            
    async def read_save_file(self, file_data:bytes) -> None:
        """Responsavel por salvar e validar o arquivo csv

        Args:
            file_data (bytes): o arquivo csv

        Raises:
            Exception: lança um excepion caso o arquivo csv nao contivar toda as colunas no padrao
        """
        
        
        file_path = Path(f"{self.upload_path}/{uuid4()}.csv")
        
        with open(str(file_path), "wb") as csv_file:
            csv_file.write(file_data)
            
            csv_file.close()
            
        data = []
        
        with open(str(file_path), "r+") as  csv:
            for row in DictReader(csv, delimiter=";"):
                data.append(row)
                
        keys = [
            "name",
            "url_site",
            "url_linkedin",
            "url_instagram",
            "url_x"
        ] 
                
                
        publish = RabbitPublish()
        
        for dict_data in data:
            for key in keys:
                if not key in dict_data:
                    file_path.unlink()
                    raise Exception(f"Arquivos CSV fora do padrão, a coluna {key} não esta presente")

            await publish.publish_one(dict_data)
        
        publish.channel.close()
   