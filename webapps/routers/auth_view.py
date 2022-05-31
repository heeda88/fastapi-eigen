from fastapi import APIRouter,Request, Response, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from jose import jwt

from database import get_db
from models import User
from hashing import Hasher
from settings import settings

router= APIRouter(include_in_schema=False)


templates=Jinja2Templates(directory="templates")


@router.get("/login")
def login(request:Request):
	return templates.TemplateResponse(name="user_login.html",context={"request":request})

@router.post("/login")
async def login(response:Response, request:Request, db:Session=Depends(get_db)):
	form = await request.form()
	email=form.get("email")
	password=form.get("password")
	errors=[]
	if not email:
		errors.append("Please enter valid email")
	if len(password)<=6:
		errors.append("please enter valid password")
		return templates.TemplateResponse(name="user_login.html",context={"request":request, "errors":errors})
	try:
		user = db.query(User).filter(User.email==email).first()
		if user is None:
			errors.append("Email does note exist.")
			return templates.TemplateResponse(name="user_login.html",context={"request":request, "errors":errors})
		else :
			if Hasher.verify_password(plain_password=password, hash_password=user.hashed_password):
				data={}
				data['email']= user.email
				jwt_token= jwt.encode(claims=data,key=settings.SC_KEY, algorithm=settings.PW_ENCODE)
				msg = "Login successful"
				response=templates.TemplateResponse(name="user_login.html",context={"request":request, "msg":msg})
				response.set_cookie(key="access_token", value=f"Bearer {jwt_token}",httponly=True)
				return response
			else :
				errors.append("Password is incorrect.")
				return templates.TemplateResponse(name="user_login.html",context={"request":request, "errors":errors})
	except IntegrityError as e:
		errors.append(e)
		return templates.TemplateResponse(name="user_login.html",context={"request":request, "errors":errors})

	