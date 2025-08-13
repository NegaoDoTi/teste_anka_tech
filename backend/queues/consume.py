from pika import BlockingConnection, URLParameters
from config.env import RABBITMQ_URL, RABBIT_QUEUE
from json import loads


class RabbitConsume:
    
    def __init__(self):
        self.__parameters = URLParameters(RABBITMQ_URL)
        self.__connection = BlockingConnection(self.__parameters)
        
        self.channel = self.__connection.channel()
                
    async def consume_one(self) -> dict | None:
        method_frame, header_frame, body = self.channel.basic_get(queue=RABBIT_QUEUE)
        
        if method_frame:
            message = body.decode("utf-8")
            
            self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            
            message = loads(message)
            
            return message
        
        else:
            print("Sem mensagens para consumir, fila vazia!")
            return None
        
    async def check_message_count(self) -> int:
        
        queue_info = self.channel.queue_declare(RABBIT_QUEUE, passive=True)
        
        return queue_info.method.message_count