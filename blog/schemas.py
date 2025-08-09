from pydantic import BaseModel, Field
from datetime import datetime


class BlogPostCreate(BaseModel):
    title : str = Field(..., title="Title of the blog post", max_length=255)
    content: str = Field(..., title="Content of the blog post")
    
class BlogUpdate(BlogPostCreate):
    pass

class BlogResponse(BlogPostCreate):
    id: int = Field(..., title="Unique identifier of the blog post")
    author_id: int = Field(..., title="ID of the author of the blog post")
    is_published: bool = Field(default=False, title="Publication status of the blog post")
    avg_rating: float = Field(default=0.0, title="Average rating of the blog post")
    author_id : int
    created_at: datetime = Field(..., title="Creation timestamp of the blog post")
    updated_at: datetime = Field(..., title="Last update timestamp of the blog post")

    class Config:
        orm_mode = True
    