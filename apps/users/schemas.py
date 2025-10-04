from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    last_name: str
