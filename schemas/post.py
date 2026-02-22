from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from schemas.user import UserResponse
from schemas.category import CategoryResponse

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    category_ids: List[int] = []

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_ids: Optional[List[int]] = None

class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: Optional[datetime] = None
    author: Optional[UserResponse] = None
    categories: List[CategoryResponse] = []

    class Config:
        from_attributes = True