from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True

class NewsBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class NewsCreate(NewsBase):
    tags: List[str] = []

class NewsUpdate(NewsBase):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class News(NewsBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[Tag] = []

    class Config:
        from_attributes = True 