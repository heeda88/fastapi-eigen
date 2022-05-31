from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from routers import testing, users, items, login
from webapps.routers import item_view, user_view, auth_view
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)


route_description="""

HeedaApp API helps you do awesome stuff. 🚀


[Home](/home) \n
[Docs](/docs) \n
[Redoc](/redoc)

### Refs
FastAPI :
[https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/) \n
uvicorn :
[https://www.uvicorn.org/](https://www.uvicorn.org/) \n
sqlalchemy:
[https://docs.sqlalchemy.org/](https://docs.sqlalchemy.org/) \n

### To Do
### Done
* **Router set**
* **Access DB**
* **Session generate**
* **Create table**
* **Create users** 
* **if note exists DB, then Create new DB** 
* **Read users** 
* **Create Items** 
* **Read Items** 


### Items
To do :
done :


### Users
To do :
done :
"""

tag_metadata=[
	{'name':'testing', 'description':'This is testing route.'},
	{'name':'users', 'description':'This is users route.'},
	{'name':'items', 'description':'This is items route.'},
]


severs=[
	{
			"url": "/api/v1"
	},
	{
			"url": "https://stag.example.com",
			"description": "Staging environment"
	},
	{
			"url": "https://prod.example.com",
			"description": "Production environment"
	}
]


app = FastAPI(
	title="MyTesting",
	description=route_description,
	version='0.0.1',
	contact={'name':'d_coding'},
	openapi_tags=tag_metadata,
	servers=severs,
)

app.mount(path="/static",app=StaticFiles(directory="static"), name='static')

app.include_router(testing.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(login.router)
app.include_router(item_view.router)
app.include_router(user_view.router)
app.include_router(auth_view.router)



