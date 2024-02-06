from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field
from datetime import datetime

class AppSettings(BaseSettings):
    api_port: int | None = 8000
    data_dir: str | None = "./data"

class User(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    admin:bool | None = False
    age: int | None = None
    gender: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
