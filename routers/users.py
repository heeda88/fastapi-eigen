from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from datetime import datetime

from schemas import UserCreate, UserShow, UserRoleUpdate
from models import User
from database import get_db
from hashing import Hasher

router=APIRouter()

"""
users

"""

@router.get('/users/get_users', tags=['users'])
def getuser(db: Session=Depends(get_db)):
	user_session=db.query(User.email)
	return user_session.all()

@router.get('/users/get_user/{user_id}', tags=['users'])
def getuser(db: Session=Depends(get_db), user_id:int=Path(...)):
	user_session=db.query(User.email)
	return user_session.all()[user_id]

@router.post('/users/create_user/', tags=['users'], response_model=UserShow )
def create_user(user:UserCreate,db:Session=Depends(get_db)):
	add_user=User(email=user.email, hashed_password=Hasher.get_hash_password(user.password),reg_date=datetime.now())
	db.add(add_user)
	db.commit()
	db.refresh(add_user)
	return add_user

@router.post('/users/nominate', tags=['users'])
def nominate_role(role:UserRoleUpdate, db:Session=Depends(get_db)):
	user_session=db.query(User).filter(User.id==role.id)
	if not user_session.all():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f' User id {role.id} does not exist')
	user_session.update(role.dict())
	db.commit()
	return  user_session.all()


@router.delete('/users/delete/{user_id}',tags=['users'])
def delete_user(user_id:int, db:Session=Depends(get_db)):
	user_session=db.query(User).filter(User.id==user_id)
	if not user_session.all():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f' User id {user_id} does not exist')
	user_session.delete()
	db.commit()
	return {"message": f'User id {user_id} delete then the user does not exist.'}

