from time import sleep
from scripts.robot.start import StartScript
from queues.consume import RabbitConsume
import asyncio

def run() -> None:
    """Metodo responsavel por iniciar o robo de scraping
    """
    
    script = StartScript()
    
    script.start()
    
    print("Processamento iniciado com sucesso!")
    
    return
    
if __name__ == "__main__":
    while True:
        consumer = RabbitConsume()
        
        number = asyncio.run(consumer.check_message_count())
        
        consumer.channel.close()
        
        if number > 0:
            run()
            
        sleep(5)
        