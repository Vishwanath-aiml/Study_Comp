from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()  # Like BaseModel in pydantic but slightly different

class Product(Base):    # Create a structure for the sql to read as our Class has datatypes of python and not of sql

    __tablename__ = "Product"

    id = Column(Integer, primary_key = True) # Here no need of index = True as primary key does indexing
    name = Column(String)  # if u add index = True then there will be two indexes this one and primary key
    age = Column(Integer)