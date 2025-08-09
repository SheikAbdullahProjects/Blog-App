from fastapi import APIRouter, Depends, Path
from typing import List, Annotated
from .models import Blog
from auth.models import User
from database import get_db
from sqlalchemy.orm import Session
from starlette import status
from .schemas import BlogResponse, BlogPostCreate, BlogUpdate
from .service import get_blogs, create_blog as create_blog_srv, get_blog_by_id as get_blog_by_id_srv, check_blog_exists, check_blog_owner, update_blog as update_blog_srv, check_admin
from auth.service import get_current_user

db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(
    prefix="/blog",
    tags=["blog"]
)

@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[BlogResponse])
async def get_all_blogs(db : db_dependency):
    blogs = await get_blogs(db)
    return blogs

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=BlogResponse)
async def get_blog_by_id(db : db_dependency, token : str, id : int = Path(ge=1)):
    await get_current_user(token, db)
    blog = await get_blog_by_id_srv(db, id)
    return blog

@router.post("/create/blog", status_code=status.HTTP_200_OK, response_model=BlogResponse)
async def create_blog(db : db_dependency, token : str, blog_model : BlogPostCreate):
    user = await get_current_user(token, db)
    blog = await create_blog_srv(db, user, blog_model)
    return blog

@router.put("/update/{id}", status_code=status.HTTP_200_OK, response_model=BlogResponse)
async def update_blog(db : db_dependency, token : str, blog_model : BlogUpdate, id : int = Path(ge=1)):
    user = await get_current_user(token, db)
    blog_db = await check_blog_exists(db, id)
    await check_blog_owner(db, blog_db.id, user)
    blog = await update_blog_srv(db , blog_db, blog_model)
    return blog

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(db : db_dependency, token : str, id : int = Path(ge=1)):
    user = await get_current_user(token, db)
    blog_db = await check_blog_exists(db, id)
    await check_blog_owner(db, blog_db.id, user)
    db.delete(blog_db)
    db.commit()
    
    
    
@router.put("/publish/{id}", status_code=status.HTTP_200_OK, response_model=BlogResponse)
async def publish_blog(db : db_dependency, token : str, id : int = Path(ge=1)):
    user = await get_current_user(token, db)
    await check_admin(user)
    blog_db = await check_blog_exists(db, id)
    blog_db.is_published = True
    db.commit()
    db.refresh(blog_db)
    return blog_db