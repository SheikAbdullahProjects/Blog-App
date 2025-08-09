from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timedelta, timezone


class Blog(Base):
    __tablename__ = "blogs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    avg_rating = Column(Float, default=0.0)
    
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_published = Column(Boolean, default=False)
    created_at = Column(String, default=datetime.now(timezone.utc))
    updated_at = Column(String, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    author = relationship("User", back_populates="blogs")
    reviews = relationship("Review", back_populates="blog")