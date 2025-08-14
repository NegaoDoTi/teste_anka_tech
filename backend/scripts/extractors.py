import re
import tiktoken

def extract_relevant_chunks(html_text: str, company_name:str,  max_tokens = 700 ) -> dict:
    """Metodo responsavel por extrair AUM (patrimônio sob gestão, Assets under management) das
        paginas html se houver

    Args:
        html_text (str): html da pagina em texto
        company_name (str): nome da empresa que sera feita extração de dados da pagina
        max_tokens: numero maximo de tokens que a extração dessa pagina deve retornar

    Returns:
        dict: total de tokens que extração tem e a extração em texto
    """
    
    pattern = re.compile(r"([R$US$]?\d+[,.]\d+ \w+)", re.IGNORECASE)
    
    keywords = [
        "AUM",
        "Assets under management",
        "patrimônio sob gestão"
    ]
    
    keyword_pattern = re.compile("|".join(re.escape(k) for k in keywords ), re.IGNORECASE)
    
    matches = keyword_pattern.findall(html_text)
    
    matches_1 = pattern.findall(html_text)
    
    datas = list({m.strip() for m in matches if m.strip()})
    
    datas_1 = list({m_1.strip() for m_1 in matches_1 if m_1.strip()})
    
    relevant_texts = []
    
    for data in datas:
        relevant_texts.append(data)
        
    for data in datas_1:
        relevant_texts.append(data)
        
    relevant_texts = " ".join(relevant_texts)
    
    final_text = f"""Qual é o patrimônio sob gestão (AUM) anunciado por {company_name}, 
    informações que podem ser uteis:""" +  relevant_texts + """Responda somente com o número e 
    a unidade (ex.: R$ 2,3 bi) ou NAO_DISPONIVEL."""
    
    final_text = final_text.lower()
    
    enc = tiktoken.encoding_for_model("gpt-4o")
    tokens = enc.encode(final_text)
    
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    
    total = len(tokens)
    text = enc.decode(tokens)
    
    return {"total_tokens" : total, "prompt" : text}
    
    
    