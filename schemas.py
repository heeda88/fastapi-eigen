from errno import EMLINK
from turtle import st, update
from unicodedata import category
from pydantic import BaseModel, EmailStr
from datetime import date, datetime

"""
1. return  -> response_model
return : pydantic, response_model: pydantic
orm  모델을 거치지 않으므로 그대로 사용하면 됨

return : orm_model , respomnse_model: pydantic
pydantic model Config 인스턴스에 입력값이 orm_model 이라는 것을 알려야함 

Refs:
https://pydantic-docs.helpmanual.io/usage/models/#orm-mode-aka-arbitrary-class-instances

pydantic.BaseModel 생성 인스턴스 내부에
Config 인스턴스를 생성하게 되면 orm_mode가 활성화 되며 

class.from_orm(class).dict()
dictionary 타입으로 인수를 호출 할수 있게 된다. 

FAST_API 에서 
pydantic model로 받은 후
orm_model input -> DB session gen - > DB query ->

response_model 호출시에  return 인스턴스를 에서
dict().keys()   키값을 str로 받은수 

respose_model[f'{key}']= return_orm_model.key
"""


"""
Create

"""
class UserCreate(BaseModel):
	email:EmailStr
	password:str

class UserShow(BaseModel):
	email:EmailStr
	is_active:bool

	class Config:
		orm_mode=True

class UserRoleUpdate(BaseModel):
	id:int
	role:str

class ItemCreate(BaseModel):
	title:str
	description:str

class ItemShow(BaseModel):
	title:str
	description:str
	create_date:datetime
	create_user:int
	update_date:datetime
	update_user:int

	class Config:
		orm_mode=True

class ItemUpdate(BaseModel):
	title:str
	description:str
	category:str