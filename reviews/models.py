from sqlalchemy import Column, String, Integer, Text, ForeignKey, Float
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from database import Base

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float, nullable=False)
    review_content = Column(Text, nullable=False)

    created_at = Column(String, default=datetime.now(timezone.utc))
    updated_at = Column(String, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    blog_id = Column(Integer, ForeignKey("blogs.id"), nullable=False)

    reviewer = relationship("User", back_populates="reviews")
    blog = relationship("Blog", back_populates="reviews")