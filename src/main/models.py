from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field
from datetime import datetime

class AppSettings(BaseSettings):
    api_port: int | None = 8000
    data_dir: str | None = "./data"
    mongohost: str | None = "localhost"
    mongoport: int | None = 27017

class User(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    admin:bool | None = None
    age: int | None = None
    gender: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    email: str | None = None
    username: str | None = None 
    password: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

