from fastapi.testclient import TestClient
from ..app import app
from pathlib import Path
import io

client = TestClient(app)

def test_upload_route_sucess():
    """Teste sucesso ao enviar aquivo para rota upload
    """
    
    file_path = Path(Path(__file__).parent, "companies.csv")
    
    with open(str(file_path), "rb") as csv_file:
        encoded_file = io.BytesIO(csv_file.read())
        
        csv_file.close()
        
    response = client.post("/upload", files= {"file" : ("companies.csv", encoded_file, "text/csv" )})

    assert response.status_code == 201
    assert response.json() == {"message" : "Sucesso, arquivo enviado para fila, a extração de dados começará em breve"}

def test_upload_route_fail():
    """Teste a rota upload ao enviar arquivo csv fora do padrao
    """
    
    fail_path = Path(Path(__file__).parent, "companies_fail.csv")
    
    with open(str(fail_path), "rb") as csv_file:
        encoded_file = io.BytesIO(csv_file.read())
        
        csv_file.close()
        
    response = client.post("/upload", files= {"file" : ("companies_fail.csv", encoded_file, "text/csv" )})

    assert response.status_code == 400
    assert response.json() == {"message" : "Arquivos CSV fora do padrão, a coluna url_linkedin não esta presente"}
    
def test_upload_route_file_type():
    """Testa a rota ao enviar um aquivo que não é csv
    """
    
    txt_file_path = Path(Path(__file__).parent, "companies.txt")
    
    with open(str(txt_file_path), "rb") as text_fle:
        encoded_file = io.BytesIO(text_fle.read())
        
        text_fle.close()
        
    response = client.post("/upload", files= {"file" : ("companies.txt", encoded_file, "text/plain" )})
    
    assert response.status_code == 400
    assert response.json() == {"message" : "Só é aceito arquivos do tipo CSV"}
    
def test_usage_route_sucess():
    """Testa a rota usage
    """
    
    response = client.get("/usage/today")
    
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], dict)
    assert "usage" in response.json()["data"]
    assert isinstance(response.json()["data"]["usage"], list)
    
    
def test_usage_route_post():
    """Testa a rota usage/today no metodo http post para faze o rescrape
    """
    
    respose = client.post("/usage/today")
    
    assert respose.status_code == 200
    assert "message" in respose.json()
    assert isinstance(respose.json()["message"], str)
    assert respose.json()["message"] == "Sucesso"