

from time import timezone
from sqlalchemy import Column, DateTime,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from database import Base


"""
1. indenx 기능 설정
	검색해야 하는 항목이 있다면 DB 쿼리 속도를 높이기 위하여,
	인덱스 기능을 True로 설정해야한다.
	해당 기능설정시 Index 파일을 색인하여 검색속도를 높힌다.
	Table record 색인 보다 대체적으로 빠름
	ex) Coulmn( ....., index= True)

2. 외래키 설정
	외래키 지정을 위해서 각 parameter 인수명을 정확히 지정하려고 했지만
	ForeignKey 같은경우  필수 지정인수로 지정되어 있지 않으며,
	kwargs 인스턴스 타입 매칭후   
	Column  인수 생성자로 집함.
	즉, 인수지정이 안됨

	query문 같은 경우 
	sqlalchemy.create_engine.connection()
	sqlalchemy.create_engine.beging()
	아래와 같은 명령어를 통해서 직접 생산이 가능함

	sql.query 제공하는 방식으로는 학습곡선이 요구 되며 재사용성이 떨어짐

3. Base 상속시
	해당 인스턴스는 orm 인스턴스

"""

class User(Base):
	__tablename__='users'
	id=Column(name='id',type_=Integer,primary_key=True,index= True)
	email=Column(name='email',type_=String, unique=True, nullable=False, index=True )
	reg_date=Column(name='reg_date',type_=DateTime(timezone=True), nullable=False)
	role=Column(name='role',type_=String, nullable=False, index=True, default='None')
	hashed_password=Column(name='hashed_password',type_=String, nullable=False)
	is_active=Column(name='is_active', type_=Boolean, nullable=False,default=True)
	items=relationship(argument='Item',back_populates='owner')

class Item(Base):
	__tablename__='items'
	id=Column(name='id',type_=Integer,primary_key=True, index=True)
	create_user = Column('create_user',Integer,ForeignKey('users.id'))
	create_date = Column(name='create_date',type_=DateTime(timezone=True), nullable=False)
	update_user = Column('update_user', Integer)
	update_date = Column(name='update_date',type_=DateTime(timezone=True), nullable=False)
	category=Column(name='category', type_=String, nullable=False, default='None')
	title=Column(name='title',type_=String, nullable=False, index=True)
	description=Column(name='description', type_=String, nullable=False, index=True)
	is_active=Column(name='is_active', type_=Boolean, nullable=False,default=True)
	owner=relationship(argument='User', back_populates='items')
