from sqlite3 import IntegrityError
from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from datetime import datetime

from hashing import Hasher
from models import  User
from database import get_db

router = APIRouter(include_in_schema=False)
template = Jinja2Templates(directory='templates')

@router.get("/register")
def registration(request:Request):
	return template.TemplateResponse(name="user_register.html", context={"request":request})


@router.post('/register')
async def registration(request: Request, db: Session=Depends(get_db)):
	form = await request.form()
	email=form.get("email")
	password=form.get("password")
	errors=[]
	if len(password)<=6:
		errors.append("Password should be > 6 character")
		return template.TemplateResponse(name="user_register.html", context={"request":request, "errors":errors})

	add_user= User(email=email, hashed_password=Hasher.get_hash_password(password), reg_date=datetime.now())
	try:
		db.add(add_user)
		db.commit()
		db.refresh(add_user)
		return responses.RedirectResponse(url="/home?msg=Successfully Registered",status_code=status.HTTP_302_FOUND)
	except IntegrityError:
		errors.append("Email already exist")
		return template.TemplateResponse(name="user_register.html", context={"request":request, "errors":errors})
