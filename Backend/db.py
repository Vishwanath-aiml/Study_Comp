from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import db_models
from models import Product

products = [
    Product(id = 1, name="Sam", age = 19),
    Product(id = 2, name="Ram", age = 18)
]

db_url = "postgresql://postgres:1234@localhost:5432/NITD_db"  # which sql is used
engine = create_engine(db_url)  # do the thing
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    '''This is created so that we dont need to manually create session everytime in a function 
       and also to make sure that the session is closed after the function is executed'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = SessionLocal()  # Create a session

    count = db.query(db_models.Product).count()  # so that it doesnt add when table is already having these things( basic version needs to change)
    if count == 0:
        for i in products:                               # in next line to specidy which table u need to write db_mdels.(Class name of the table)
            db.add(db_models.Product(**i.model_dump()))  # ** is for unpacking and model_dump is to convert it to dictionary format to be able to unpack
    
    db.commit() # Because auto commit was disabled