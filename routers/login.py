__author__='heeda'

"""


	## authentification : who the user is ? (신원 확인)

1. Basic : use of session and cookies
2. JWT :Identify user and send them token and for further request, verify token data
3. OAuth2: identify using 3rd party (Facebook, Google, GitHub)
4. OpenID connect =? (extension of OAuth2)


## authorization : whether the user has particular access or not ?  (권한 위임)
fastapi.security



1. User post Form(email, password) to webserver.
2. If exists email, then DB_query load user data.
3. verify password
4. create token that basis user.email or user.name  is uniqued
5. Send toekn 

## Authentification type
Basic
사용자 아이디와 암호를 Base64로 인코딩한 값을 토큰으로 사용한다. (RFC 7617)

Bearer
JWT 혹은 OAuth에 대한 토큰을 사용한다. (RFC 6750)

Digest
서버에서 난수 데이터 문자열을 클라이언트에 보낸다. 클라이언트는 사용자 정보와 nonce를 포함하는 해시값을 사용하여 응답한다 (RFC 7616)

HOBA
전자 서명 기반 인증 (RFC 7486)

Mutual
암호를 이용한 클라이언트-서버 상호 인증 (draft-ietf-httpauth-mutual)

AWS4-HMAC-SHA256
AWS 전자 서명 기반 인증 




"""





from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt

from database import get_db
from hashing import Hasher
from models import User
from settings import settings




oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/login/token")



router = APIRouter()


@router.post("/login/token/", tags=["login"])
def retrieve_token_after_authentification(form_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
	user=db.query(User).filter(User.email==form_data.username).first()
	if  not user:	
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f' Invalid email')
	if not Hasher.verify_password(plain_password=form_data.password, hash_password=user.hashed_password):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f' Invalid password')
	data= {}
	data['id']=user.id
	data['email']=user.email
	data['role']=user.role
	data['reg_date']=user.reg_date.strftime("%m/%d/%Y, %H:%M:%S")
	
	jwt_token= jwt.encode(claims=data,key=settings.SC_KEY, algorithm=settings.PW_ENCODE)

	return {"access_token" : jwt_token , "token_type" : "bearer"}



