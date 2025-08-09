from fastapi import HTTPException
from .models import Review
from auth.models import User
from blog.models import Blog
from starlette import status
from sqlalchemy.orm import Session
from .schemas import ReviewCreate
from sqlalchemy import func


async def check_already_reviewed(db : Session, user, blog):
    review_exists = db.query(Review).filter(Review.blog_id == blog.id, Review.reviewer_id == user.id).first()
    if review_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Review already present")
    
async def check_review_exists(db : Session, blog, id : int):
    review = db.query(Review).filter(Review.id == id, Review.blog_id == blog.id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review

async def check_review_owner(db : Session, user, blog, id : int):
    review = await check_review_exists(db, blog, id)
    print(review.reviewer_id, user.id)
    if review.reviewer_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this review")
    return review

async def update_avg_rating(db, blog):
    avg_rating = db.query(func.avg(Review.rating)).filter(Review.blog_id == blog.id).scalar()
    blog.avg_rating = round(avg_rating, 2) if avg_rating else 0.0
    db.commit()
    db.refresh(blog)

async def create_review(db : Session, user, blog,  review_model : ReviewCreate):
    review = Review(reviewer_id=user.id,blog_id=blog.id, **review_model.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    await update_avg_rating(db, blog)
    return review

async def get_review_by_id(db : Session, blog, id : int):
    review = db.query(Review).filter(Review.id == id, Review.blog_id == blog.id).first()
    return review
    
async def get_all_reviews(db : Session, blog):
    reviews = db.query(Review).filter(Review.blog_id == blog.id).all()
    return reviews

async def update_review(db : Session, blog, review, review_model : ReviewCreate):
    review.rating = review_model.rating
    review.review_content = review_model.review_content
    db.commit()
    db.refresh(review)
    await update_avg_rating(db, blog)
    return review


    