from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.googlesearch import GoogleSearchTools
from config.env import OPENAI_API_KEY

class ChatGPTAgent():
    """Agente ChatGPT
    """
    
    def __init__(self):
        self.agent: Agent
        self.max_output_tokens = 800
        self.dayli_max_cost = 15.00
        self.get_agent()
        
    def get_agent(self) -> None:
        """Cria o Agente LLM usando lib agno
        """
        
        self.agent= Agent(
            name="Agente de finanças",
            role="Assistente para buscar e fornecer informações detalhadas e confiáveis sobre finanças de empresas",
            model=OpenAIChat(id="gpt-4o", api_key=OPENAI_API_KEY, max_tokens=self.max_output_tokens),
            tools=[DuckDuckGoTools(), GoogleSearchTools()],
            instructions=(
                "Forneça respostas resumidas, claras e baseadas em fontes confiáveis."
                "Use a ferramenta DuckDuckGo e Google para obter dados atualizados. "
                "Lembre-se do contexto das interações anteriores."
                "Converter valores (mi, bi) para número dec‑float padronizado (ex.: 2.3e9)"
            ),
            show_tool_calls=True,
            stream=False
        )
    
    def ask_the_agent(self, prompt:str, total_tokens:int, now_day_cost:float) -> dict[float, str]:
        """Metodo responsavel por perguntar o Agente LLM

        Args:
            prompt (str): Pergunta a ser enviada para o Agente LLM
            total_tokens (int): Tamanho da pergunta em tokens
            now_day_cost (float): Total de custos ja gastos no dia atual antes dessa pergunta

        Returns:
            dict[float, str]: retornar o valor dessa pergunta + valor da reposta do LLM e a respota do LLM
        """
        
        
        task_cost = self.calculate_cost(total_tokens)
        
        check = self.check_budget_and_run(now_day_cost=now_day_cost, task_cost=task_cost)
        
        if not check:
            return {
                "message" : "Não foi possivel perguntar o Agente porque o limite diario foi atingido"
            }
        
        result = self.agent.run(message=prompt, stream=False)
        
        return {"task_cost" : task_cost, "message" : result.content}
    
    def calculate_cost(self, prompt_tokens:int) -> float:
        """Calcula mais ou menos quantos custa fazer essa pergunta ao LLM

        Args:
            prompt_tokens (int): Tamanho da pergunta em tokens

        Returns:
            float: valor total da pergunta
        """
    
        input_token_cost = 5.00/1000000
        output_token_cost = 15.00/1000000
        
        prompt_cost = prompt_tokens * input_token_cost
        
        result_cost = self.max_output_tokens * output_token_cost

        task_cost = prompt_cost + result_cost
        
        return task_cost
    
    def check_budget_and_run(self, now_day_cost:float, task_cost:float) -> bool:
        """Valida se essa pergunta + resposta custará mais caro que o valor diario dispovel

        Args:
            now_day_cost (float): Total de custos ja gastos no dia atual
            task_cost (float): valor da pergunta + resposta

        Returns:
            bool: Se for true permitido perguntar ao Agente LLM, se nao false
        """
        if now_day_cost + task_cost >= self.dayli_max_cost:
            return False
        
        return True
