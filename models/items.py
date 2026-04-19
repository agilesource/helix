"""Data models"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ItemsBase(BaseModel):
    id: str

class Items(ItemsBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ItemsCreate(ItemsBase):
    pass

class ItemsUpdate(BaseModel):
    pass
