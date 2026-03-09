from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:1234@localhost:5432/NITD_db"  # which sql is used
engine = create_engine(db_url)  # do the thing
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)