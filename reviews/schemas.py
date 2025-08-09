from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime



class ReviewCreate(BaseModel):
    rating : int = Field(ge=1)
    review_content : str
    

class ReviewResponse(ReviewCreate):
    id : int
    created_at : datetime
    updated_at : datetime
    reviewer_id : int
    blog_id : int
    
    model_config = ConfigDict(from_attributes=True)
