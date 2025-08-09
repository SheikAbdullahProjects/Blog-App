from database import Base
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .enums import Role


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String)
    role = Column(Enum(Role), default=Role.USER)
    hashed_password = Column(String, nullable=False)
    
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    blogs = relationship("Blog", back_populates="author")
    reviews = relationship("Review", back_populates="reviewer")
    
    