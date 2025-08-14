from pydantic import BaseModel

class UsageResponse(BaseModel):
    data: dict
    
class UsageResponseFail(BaseModel):
    message: str
    
class UsageRescrapeResponse(BaseModel):
    message: str