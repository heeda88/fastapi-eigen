
#%%
from dotenv import load_dotenv
import os

load_dotenv('.env')


class Settings:
	def __init__(self) -> None:
		self.DB_TYPE=os.getenv('DB_TYPE')
		self.DB_NAME=os.getenv('DB_NAME')
		self.DB_USER=os.getenv('DB_USER')
		self.DB_PASW=os.getenv('DB_PASW')
		self.DB_HOST=os.getenv('DB_HOST')
		self.DB_PORT=os.getenv('DB_PORT')
		self.DB_URL=f"{self.DB_TYPE}://{self.DB_USER}:{self.DB_PASW}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
		# self.DB_URL=f"sqlite:///./sql_app.db" # sqllite3
		self.SC_KEY =os.getenv('SC_KEY')
		self.PW_ENCODE='HS256'
settings=Settings()