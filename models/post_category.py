from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database import Base

class PostCategory(Base):
    __tablename__ = "posts_category"

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    cat_id = Column(Integer, ForeignKey("category.id"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('post_id', 'cat_id'),
    )

    post = relationship("Post", back_populates="categories")
    category = relationship("Category", back_populates="posts")