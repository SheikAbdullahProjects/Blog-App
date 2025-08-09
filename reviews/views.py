from fastapi import APIRouter, HTTPException, Depends, Path
from typing import Annotated, List
from starlette import status
from sqlalchemy.orm import Session
from auth.service import get_current_user
from blog.service import get_blog_by_id
from database import get_db
from .schemas import ReviewResponse, ReviewCreate
from .service import create_review as create_review_srv, check_already_reviewed, get_all_reviews, get_review_by_id, check_review_owner, update_review as update_review_srv


db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(
    prefix="/review",
    tags=["review"]
)

@router.get("/all/{id}", status_code=status.HTTP_200_OK, response_model=List[ReviewResponse])
async def get_reviews(db : db_dependency, token : str, id : int = Path(ge=1)):
    user = await get_current_user(token, db)
    blog = await get_blog_by_id(db , id)
    reviews = await get_all_reviews(db, blog)
    return reviews
@router.get("/all/{blog_id}/review/{review_id}", status_code=status.HTTP_200_OK, response_model=ReviewResponse)
async def get_reviews(db : db_dependency, token : str, blog_id : int = Path(ge=1), review_id : int = Path(ge=1)):
    user = await get_current_user(token, db)
    blog = await get_blog_by_id(db , blog_id)
    review = await get_review_by_id(db, blog, review_id)
    return review

@router.post("/create-review/{blog_id}", status_code=status.HTTP_201_CREATED, response_model=ReviewResponse)
async def create_review(db : db_dependency, token : str, review_model : ReviewCreate, blog_id : int = Path(ge=1)):
    user = await get_current_user(token, db)
    blog = await get_blog_by_id(db , blog_id)
    await check_already_reviewed(db, user, blog)
    review = await create_review_srv(db, user, blog, review_model)
    return review

@router.put("/update/{blog_id}/review/{review_id}", status_code=status.HTTP_200_OK, response_model=ReviewResponse)
async def update_review(db : db_dependency, token : str, review_model : ReviewCreate, blog_id : int = Path(ge=1), review_id : int = Path(ge=1)):
    user = await get_current_user(token, db)
    blog = await get_blog_by_id(db , blog_id)
    review = await check_review_owner(db, user, blog, review_id)
    updated_review = await update_review_srv(db , blog, review, review_model)
    return updated_review
    
@router.delete("/delete/{blog_id}/review/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(db : db_dependency, token : str, blog_id : int = Path(ge=1), review_id : int = Path(ge=1)):
    user = await get_current_user(token, db)
    blog = await get_blog_by_id(db , blog_id)
    review = await check_review_owner(db, user, blog, review_id)
    db.delete(review)
    db.commit()
    
    
