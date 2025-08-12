from fastapi.testclient import TestClient
from ..app import app
from pathlib import Path
import io

client = TestClient(app)

def test_upload_route_sucess():
    
    file_path = Path(Path(__file__).parent, "companies.csv")
    
    with open(str(file_path), "rb") as csv_file:
        encoded_file = io.BytesIO(csv_file.read())
        
        csv_file.close()
        
    response = client.post("/upload", files= {"file" : ("companies.csv", encoded_file, "text/csv" )})

    assert response.status_code == 201
    assert response.json() == {"message" : "Sucesso, arquivo enviado para fila, a extração de dados começará em breve"}

def test_upload_route_fail():
    
    fail_path = Path(Path(__file__).parent, "companies_fail.csv")
    
    with open(str(fail_path), "rb") as csv_file:
        encoded_file = io.BytesIO(csv_file.read())
        
        csv_file.close()
        
    response = client.post("/upload", files= {"file" : ("companies_fail.csv", encoded_file, "text/csv" )})

    assert response.status_code == 400
    assert response.json() == {"message" : "Arquivos CSV fora do padrão, a coluna url_linkedin não esta presente"}
    
def test_upload_route_file_type():
    
    txt_file_path = Path(Path(__file__).parent, "companies.txt")
    
    with open(str(txt_file_path), "rb") as text_fle:
        encoded_file = io.BytesIO(text_fle.read())
        
        text_fle.close()
        
    response = client.post("/upload", files= {"file" : ("companies.txt", encoded_file, "text/plain" )})
    
    assert response.status_code == 400
    assert response.json() == {"message" : "Só é aceito arquivos do tipo CSV"}