from fastapi import APIRouter, Depends, HTTPException, Path , status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from jose import jwt

from database import get_db
from models import Item
from schemas import ItemCreate, ItemShow, ItemUpdate
from settings import settings
from routers.login import oauth2_scheme


router=APIRouter()
"""
itme
"""

@router.post("/items/item_create",tags=['items'],response_model=ItemShow)
def create_item(item:ItemCreate, db:Session=Depends(get_db), token:str=Depends(oauth2_scheme)):
	try:
		payload=jwt.decode(token=token,key=settings.SC_KEY, algorithms=[settings.PW_ENCODE])
	except Exception as e:
		print(e)
	now_time=datetime.now()
	add_item=Item(**item.dict(), create_date=now_time,create_user=payload['id'], update_user=payload['id'], update_date=now_time)
	db.add(add_item)
	db.commit()
	db.refresh(add_item)
	return add_item


@router.get("/items/all", tags=['items'],response_model=List[ItemShow])
def get_items(db: Session=Depends(get_db)):
	result=db.query(Item)
	if not result.all():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item does not exist")	
	return result.all()


@router.get("/items/get_title", tags=['items'])
def get_items(db: Session=Depends(get_db)):
	result=db.query(Item.title,Item.create_user)
	if not result.all():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item does not exist")	
	return result.all()


@router.get("/itmes/get/{item_id}",tags=['items'])
def get_items(db:Session=Depends(get_db),item_id:int=Path(...)):
	result=db.query(Item).filter(Item.id==item_id)
	if not result.all():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {item_id} does not exist")
	return result.all()


@router.get("/itmes/getbyuser/",tags=['items'])
def get_items(db:Session=Depends(get_db), token:str=Depends(oauth2_scheme)):
	try:
		payload=jwt.decode(token=token,key=settings.SC_KEY, algorithms=[settings.PW_ENCODE])
	except Exception as e:
		print(e)
	result=db.query(Item).filter(Item.create_user==payload['id'])
	if not result.all():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Owner {payload['id']} does not exist")
	return result.all()


@router.put('/item/update/{item_id}',tags=['items'])
def update_items(item:ItemUpdate , item_id:int, db:Session=Depends(get_db), token:str=Depends(oauth2_scheme)):
	"""
	#### how to use update \n
	sess.query(User).filter(User.age == 25).\
	update({User.age: User.age - 10}, synchronize_session=False)

	sess.query(User).filter(User.age == 25).\
	update({"age": User.age - 10}, synchronize_session='evaluate')

	dict 형태로 업데이트 함
	ex)
	result.update(jsonable_encoder(item))
	result.update(item.dict())
	result.update(item.__dict__)
	"""
	try:
		payload=jwt.decode(token=token,key=settings.SC_KEY, algorithms=[settings.PW_ENCODE])
	except Exception as e:
		print(e)
	result= db.query(Item).filter(Item.id==item_id)
	if not result.all():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item id {item_id} does not exist")
	if not result.first().create_user==payload['id']:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"This Item is not yours.")
	now_time=datetime.now()
	result.update(item.dict())
	result.update({Item.update_date: now_time})
	db.commit()
	return result.all()


@router.delete('/items/delete/{item_id}',tags=['items'])
def delete_item(item_id:int, db:Session=Depends(get_db), token:str=Depends(oauth2_scheme)):
	try:
		payload=jwt.decode(token=token,key=settings.SC_KEY, algorithms=[settings.PW_ENCODE])
	except Exception as e:
		print(e)
	item_session=db.query(Item).filter(Item.id==item_id)
	if not item_session.all():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f' Item id {item_id} does not exist')
	if not item_session.first().create_user==payload['id']:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'This Item is not yours')
	item_session.delete()
	db.commit()
	return {"message": f'Item id {item_id} delete then the user does not exist.'}