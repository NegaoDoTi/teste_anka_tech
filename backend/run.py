from time import sleep
from threading import Thread, enumerate
from scripts.robot.start import StartScript
from queues.consume import RabbitConsume
import asyncio

def run() -> None:
    
    threads_online = enumerate()
    
    threads_name = [thread_o.name for thread_o in threads_online]
    
    if "script_ia" in threads_name:
        print("Ja existe um procesos em andamento")
        return
    
    script = StartScript()
    
    thread = Thread(target=script.start)
    
    thread.name = "script_ia"
    
    thread.start() 
    
    print("Processamento iniciado com sucesso!")
    
    return
    
if __name__ == "__main__":
    while True:
        consumer = RabbitConsume()
        
        number = asyncio.run(consumer.check_message_count())
        
        consumer.channel.close()
        
        if number > 0:
            run()
            
        sleep(10)
        