from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

# 해당 라우터는swagger schema 에서 제외됨 
router = APIRouter(include_in_schema=False)
template = Jinja2Templates(directory='templates')

@router.get("/")
def get_Item(request:Request):
	return template.TemplateResponse(name="item_home.html",context={"request":request})