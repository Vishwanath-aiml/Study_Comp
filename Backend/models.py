from pydantic import BaseModel

class Product(BaseModel):  # BaseModel is for validation and error handling of data and lot more
    id:int
    name:str
    age:int