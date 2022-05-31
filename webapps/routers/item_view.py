from datetime import datetime
from fastapi import APIRouter, Depends, Path, Request , responses, status, UploadFile, File
from fastapi.templating import Jinja2Templates


from sqlalchemy.orm import Session
from jose import jwt
from typing import List

from models import Item, User
from database import get_db
from settings import settings

# 해당 라우터는swagger schema 에서 제외됨 
router = APIRouter(include_in_schema=False)
template = Jinja2Templates(directory='templates')

@router.get("/home")
def get_Item(request:Request, msg: str=None, db:Session=Depends(get_db)):
	items= db.query(Item).all()
	return template.TemplateResponse(name="item_home.html",context={"request":request,"items":items, "msg":msg})

@router.get("/fb",response_class=responses.RedirectResponse)
async def redirect_filebrowse():
	return "http://127.0.0.1:9001"

@router.get('/test')
async def upload_item(request: Request):
	return template.TemplateResponse(name="test.html", context={'request':request})

@router.get('/file_upload')
async def upload_item(request: Request):
	return template.TemplateResponse(name="file_upload.html", context={'request':request})

@router.post("/upload/new/")
async def post_upload( file: UploadFile = File(...)):
	print(file)
	workspace='/home/heeda-namu/workproject/heeda/Web/mytest/static/uploads/'
	# filename
	file_path = file.filename
	# image full path
	data_full_path = workspace+file_path
	print(data_full_path)

	with open(str(data_full_path), 'wb') as myfile:
			contents = await file.read()
			myfile.write(contents)
	data = {
			"data_path": file_path,
	}
	return data


@router.post("/upload/new_list/")
async def post_upload(file_list: List[UploadFile] = File(...)):

	workspace='/home/heeda-namu/workproject/heeda/Web/mytest/static/uploads/' 
	data={}

	for file in file_list:
		# filename
		file_path =file.filename
		# image full path
		data_full_path = workspace+file_path
		print(data_full_path)
		with open(str(data_full_path), 'wb') as myfile:
				contents = await file.read()
				myfile.write(contents)
		data[f'{file.filename}'] = 'Upload comlplete'

	return data


@router.get("/detail/{id}")
def item_detail(request: Request, id:int, db:Session=Depends(get_db)):
	item = db.query(Item).filter(Item.id==id).first()
	user= db.query(User).filter(User.id==item.create_user).first()
	email=user.email
	return template.TemplateResponse("item_detail.html", {'request':request, "item":item, "email":email})

@router.get("/music_list")
def music_play(request:Request):
	return template.TemplateResponse(name="music_list.html",context={'request': request})

@router.get("/music_recoder")
def music_play(request:Request):
	return template.TemplateResponse(name="music_recoder.html",context={'request': request})

@router.get("/music_play")
def music_play(request:Request):
	return template.TemplateResponse(name="music_play.html",context={'request': request})

@router.get("/music_widget")
def music_play(request:Request):
	return template.TemplateResponse(name="music_widget.html",context={'request': request})

@router.get("/music_stream")
def music_play(request:Request):
	return template.TemplateResponse(name="music_stream.html",context={'request': request})

@router.get("/stream_default")
def music_play(request:Request):
	return template.TemplateResponse(name="stream_default.html",context={'request': request})

@router.get("/stream_record")
def music_play(request:Request):
	return template.TemplateResponse(name="stream_record.html",context={'request': request})
@router.get("/stream_z")
def music_play(request:Request):
	return template.TemplateResponse(name="stream_z.html",context={'request': request})

@router.get("/create_an_item")
def create_an_item(request: Request):
	return template.TemplateResponse(name="item_create.html", context={'request':request})

@router.post("/create_an_item")
async def create_an_item(request: Request, db: Session=Depends(get_db)):
	form= await request.form()
	title=form.get("title")
	description=form.get("description")
	errors=[]
	if len(title)<=2:
		errors.append("Title should be > 2 characters ")
		return template.TemplateResponse("item_create.html", {'request':request, "errors":errors})
	if len(description)<=2:
		errors.append("Description should be > 2 characters ")
		return template.TemplateResponse("item_create.html", {'request':request, "errors":errors})
	
	try:
		token = request.cookies.get("access_token")
		if token is None:
			errors.append("You should be to login")
			return template.TemplateResponse("item_create.html", {'request':request, "errors":errors})
		else:
			scheme,_,jwt_token=token.partition(" ")
			payload=jwt.decode(token=jwt_token,key=settings.SC_KEY, algorithms=settings.PW_ENCODE)
			email=payload.get("email")
			user=db.query(User).filter(User.email==email).first()
			if user is None:
				errors.append("Your are not authenticated, kindly Create Account or Login first")
				return template.TemplateResponse("item_create.html", {'request':request, "errors":errors})
			else:
				# 생성 필수조건으로 유저 id와  업데이트 유저 업데이트 일자가 필요함 
				item= Item(
					title=title, 
					description=description, 
					create_user=user.id, 
					create_date=datetime.now(),
					update_user=user.id, 
					update_date=datetime.now()
					)
				db.add(item)
				db.commit()
				db.refresh(item)
				return responses.RedirectResponse(f"/detail/{item.id}", status_code=status.HTTP_302_FOUND)
	except Exception as e:
		print(e)
		return e 