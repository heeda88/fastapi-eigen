
#%%

from typing import Generator
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from settings import settings
from sqlalchemy_utils.functions import database_exists, create_database


if database_exists(settings.DB_URL):
	engine = create_engine(settings.DB_URL,future=True)
else :
	create_database(settings.DB_URL)
	engine= create_engine(settings.DB_URL,future=True)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()

def get_db() -> Generator:
	try:
		db=SessionLocal()
		yield db
	finally:
		db.close()

def get_conn() -> Generator:
	try:
		conn= engine.connect()
		yield conn
	finally:
		conn.close()

def get_begin() -> Generator:
	try:
		conn= engine.begin()
		yield conn
	finally:
		conn.close()




#%%
# from sqlalchemy import text
# with engine.connect() as conn:
# 	result = conn.execute(text("SELECT * FROM users"))
# 	print(result.all())