from pika import BlockingConnection, URLParameters
from config.env import RABBIT_QUEUE, RABBITMQ_URL
from json import dumps
import logging
from traceback import format_exc

class RabbitPublish:
    """Publisher do rabbit
    """
    
    def __init__(self):
        self.__parameters = URLParameters(RABBITMQ_URL)
        self.__connection = BlockingConnection(self.__parameters)
        
        self.channel = self.__connection.channel()
        
        self.channel.queue_declare(RABBIT_QUEUE, durable=True)
        
    async def publish_one(self, data:dict) -> None:
        """Metodo que publica apenas um mensagem na fila

        Args:
            data (dict): mensagem a ser enviada

        Raises:
            Exception: Trata o erro e lança outro caso não seja possivel publicar a mensagem
        """
        
        try:
            message = dumps(data)
            
            self.channel.basic_publish(exchange="", routing_key=RABBIT_QUEUE, body=message)
                        
            return
        except Exception:
            logging.error(f"{format_exc()}")
            
            raise Exception(f"Erro inesperado ao enviar dados para fila")