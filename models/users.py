"""Data models"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UsersBase(BaseModel):
    id: str

class Users(UsersBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UsersCreate(UsersBase):
    pass

class UsersUpdate(BaseModel):
    pass
