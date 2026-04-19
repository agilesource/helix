"""API routes"""
from fastapi import APIRouter, HTTPException
from typing import List
from models.users import Users, UsersCreate, UsersUpdate

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("", response_model=List[Users])
async def list_users():
    """List users"""
    # TODO: implement list query
    return []

@router.get("/{item_id}", response_model=Users)
async def get_users(item_id: str):
    """Get single users"""
    # TODO: implement get
    raise HTTPException(status_code=404)

@router.post("", response_model=Users)
async def create_users(item: UsersCreate):
    """Create users"""
    # TODO: implement create
    pass

@router.put("/{item_id}", response_model=Users)
async def update_users(item_id: str, item: UsersUpdate):
    """Update users"""
    # TODO: implement update
    raise HTTPException(status_code=404)

@router.delete("/{item_id}")
async def delete_users(item_id: str):
    """Delete users"""
    # TODO: implement delete
    return {"status": "deleted"}
