from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base
import datetime

news_tags = Table(
    'news_tags',
    Base.metadata,
    Column('news_id', Integer, ForeignKey('news.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    tags = relationship("Tag", secondary=news_tags, back_populates="news")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    news = relationship("News", secondary=news_tags, back_populates="tags") 