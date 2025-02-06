from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ....core.database import get_db
from ....schemas.news import NewsCreate, NewsUpdate, News, TagCreate, Tag
from ....models.news import News as NewsModel, Tag as TagModel

router = APIRouter()

@router.get("/", response_model=List[News])
def get_news(
    skip: int = 0,
    limit: int = 100,
    tags: List[str] = Query(default=[]),
    db: Session = Depends(get_db)
):
    news = db.query(NewsModel).filter(NewsModel.tags.in_(tags)).offset(skip).limit(limit).all()
    return news

@router.post("/", response_model=News)
def create_news(
    news: NewsCreate,
    db: Session = Depends(get_db)
):
    # Создаем или получаем существующие теги
    tags = []
    for tag_name in news.tags:
        tag = db.query(TagModel).filter(TagModel.name == tag_name).first()
        if not tag:
            tag = TagModel(name=tag_name)
            db.add(tag)
        tags.append(tag)
    
    # Создаем новость
    db_news = NewsModel(
        title=news.title,
        content=news.content,
        image_url=news.image_url,
        tags=tags
    )
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

@router.get("/{news_id}", response_model=News)
def get_news_by_id(
    news_id: int,
    db: Session = Depends(get_db)
):
    news = db.query(NewsModel).filter(NewsModel.id == news_id).first()
    if news is None:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    return news

@router.put("/{news_id}", response_model=News)
def update_news(
    news_id: int,
    news: NewsUpdate,
    db: Session = Depends(get_db)
):
    db_news = db.query(NewsModel).filter(NewsModel.id == news_id).first()
    if db_news is None:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    
    # Обновляем основные поля
    update_data = news.model_dump(exclude_unset=True)
    if "tags" in update_data:
        tags = []
        for tag_name in update_data["tags"]:
            tag = db.query(TagModel).filter(TagModel.name == tag_name).first()
            if not tag:
                tag = TagModel(name=tag_name)
                db.add(tag)
            tags.append(tag)
        db_news.tags = tags
        del update_data["tags"]
    
    for field, value in update_data.items():
        setattr(db_news, field, value)
    
    db.commit()
    db.refresh(db_news)
    return db_news

@router.get("/tags/", response_model=List[Tag])
def get_tags(
    db: Session = Depends(get_db)
):
    return db.query(TagModel).all() 