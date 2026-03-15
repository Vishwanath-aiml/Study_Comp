from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from models import Product
from db import SessionLocal, engine, get_db, init_db, products
import db_models
from auth import auth_router # For the inclusion of its router to validate its urls

import os   # Temporarily run the auth without https requirement
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # local machine provides http while google auth demands httpS

app = FastAPI()
app.include_router(auth_router)



db_models.Base.metadata.create_all(bind=engine)  # To create those tables





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
