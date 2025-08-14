from openpyxl import Workbook
from pathlib import Path

def generate_report(datas:list[dict]) -> str:
    """Metodo responsavel por gerar um relatorio em excel(xlsx)

    Args:
        datas (list[dict]): dados a serem transcritos no xlsx

    Returns:
        str: o caminho completo do relatio
    """
    
    wb = Workbook()
    
    ws = wb.active
    
    ws.append(["COMPANY_NAME", "SCRAPE_LOG_ID", "SCRAPE_START", "AUM_SNAPSHOT_ID", "AUM_SNAPSHOT_DATA"])
    
    for data in datas:
        ws.append([
            data["company_name"],
            data["scrape_log"],
            data["scrape_start"],
            data["aum_id"],
            data["aum"]
        ])
    
    path_report = Path(Path(__file__).parent.parent, "reports")
    
    if not path_report.exists():
        path_report.mkdir()
    
    report = f"{path_report}/relatorio.xlsx"
    
    wb.save(report)
    
    return report