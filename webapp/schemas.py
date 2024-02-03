from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    # id: Optional[int]
    first_name: str
    last_name: str
    # password: str
    username: str
    # account_created: Optional[str]
    # account_updated: Optional[str]


class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    password: str

class User(UserBase):
    id: int
    first_name: str
    last_name: str
    username: str
    # account_created: str
    # account_updated: str
    is_active: bool
    
    class Config:
        orm_mode = True