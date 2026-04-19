"""API routes"""
from fastapi import APIRouter, HTTPException
from typing import List
from models.items import Items, ItemsCreate, ItemsUpdate

router = APIRouter(prefix="/api/items", tags=["items"])

@router.get("", response_model=List[Items])
async def list_items():
    """List items"""
    # TODO: implement list query
    return []

@router.get("/{item_id}", response_model=Items)
async def get_items(item_id: str):
    """Get single items"""
    # TODO: implement get
    raise HTTPException(status_code=404)

@router.post("", response_model=Items)
async def create_items(item: ItemsCreate):
    """Create items"""
    # TODO: implement create
    pass

@router.put("/{item_id}", response_model=Items)
async def update_items(item_id: str, item: ItemsUpdate):
    """Update items"""
    # TODO: implement update
    raise HTTPException(status_code=404)

@router.delete("/{item_id}")
async def delete_items(item_id: str):
    """Delete items"""
    # TODO: implement delete
    return {"status": "deleted"}
