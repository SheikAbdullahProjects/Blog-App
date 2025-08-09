from fastapi import HTTPException
from sqlalchemy.orm import Session
from .models import Blog
from .schemas import BlogPostCreate, BlogUpdate
from starlette import status



async def get_blogs(db : Session):
    blogs = db.query(Blog).filter(Blog.is_published).all()
    return blogs

async def get_blog_by_id(db : Session, id : int):
    blog = await check_blog_exists(db, id)
    return blog

async def create_blog(db : Session, user_model, blog_model : BlogPostCreate):
    blog = Blog(author_id=user_model.id, **blog_model.model_dump())
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

async def check_blog_exists(db : Session, id : int):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not Found")
    return blog
    
    
async def check_blog_owner(db : Session, id : int, user):
    blog = await get_blog_by_id(db, id)
    if blog.author_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You don't have access to alter the blog")
    
async def update_blog(db : Session, blog , blog_model : BlogUpdate):
    blog.title = blog_model.title or blog.title
    blog.content = blog_model.content or blog.content
    db.commit()
    db.refresh(blog)
    return blog

async def check_admin(user):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin can only perform this action")
    
    

    