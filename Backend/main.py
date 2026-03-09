from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import Product
from db import SessionLocal, engine
import db_models

app = FastAPI()

def get_db():
    '''This is created so that we dont need to manually create session everytime in a function 
       and also to make sure that the session is closed after the function is executed'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_models.Base.metadata.create_all(bind=engine)  # To create those tables

products = [
    Product(id = 1, name="Sam", age = 19),
    Product(id = 2, name="Ram", age = 18)
]

def init_db():
    db = SessionLocal()  # Create a session

    count = db.query(db_models.Product).count()  # so that it doesnt add when table is already having these things( basic version needs to change)
    if count == 0:
        for i in products:                               # in next line to specidy which table u need to write db_mdels.(Class name of the table)
            db.add(db_models.Product(**i.model_dump()))  # ** is for unpacking and model_dump is to convert it to dictionary format to be able to unpack
    
    db.commit() # Because auto commit was disabled

init_db() # without this the function wont execute what happened to u


@app.get("/")  # function wrapper remeber this means a = wrapper(a)
def a():
    return "Welcome"


@app.get("/products")
def p(db: Session = Depends(get_db)):  # Used to "INJECT" the session of db as per rules of get_db"
    
    db_products = db.query(db_models.Product).all()
    if db_products:
        return db_products
    return "No Products Found"

@app.get("/products/{id}")
def q(id, db: Session = Depends(get_db)):
    
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).all()

    if db_product:
        return db_product

    return "Not found"
