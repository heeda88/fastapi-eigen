from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import UserCreate, UserShow
from models import User
from database import get_db
from hashing import Hasher

import sqlalchemy


router=APIRouter()


@router.get('/testing/hello', tags=['testing'])
def test_hello():
	
	return {'msg':'Hello world'}

@router.get('/testing/query',tags=['testing'])
def test_query(db:Session=Depends(get_db)):
	stmt=sqlalchemy.select(User)
	print(type(stmt))
	return str(stmt)


	# <class 'sqlalchemy.engine.cursor.CursorResult'>
	# result_query=db.execute('SELECT email FROM users')

	# <class 'sqlalchemy.orm.query.Query'>
	# result=db.query(User.email)
