from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.article import Category, Article, ArticleStatus
from app.schemas.article import CategoryCreate, CategoryUpdate, ArticleCreate, ArticleUpdate

class CategoryRepository:
    @staticmethod
    def get_by_id(db: Session, category_id: int) -> Optional[Category]:
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Category]:
        return db.query(Category).filter(Category.name == name).first()

    @staticmethod
    def list(db: Session) -> List[Category]:
        return db.query(Category).all()

    @staticmethod
    def create(db: Session, obj_in: CategoryCreate) -> Category:
        db_obj = Category(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(db: Session, db_obj: Category, obj_in: CategoryUpdate) -> Category:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete(db: Session, category_id: int):
        db_obj = db.query(Category).filter(Category.id == category_id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

class ArticleRepository:
    @staticmethod
    def get_by_id(db: Session, article_id: int) -> Optional[Article]:
        return db.query(Article).filter(Article.id == article_id).first()

    @staticmethod
    def list_published(db: Session, skip: int = 0, limit: int = 100) -> List[Article]:
        return db.query(Article).filter(Article.status == ArticleStatus.PUBLISHED).offset(skip).limit(limit).all()

    @staticmethod
    def list_all(db: Session, skip: int = 0, limit: int = 100) -> List[Article]:
        return db.query(Article).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, obj_in: ArticleCreate, author_id: int) -> Article:
        db_obj = Article(
            **obj_in.model_dump(),
            author_id=author_id,
            status=ArticleStatus.DRAFT
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(db: Session, db_obj: Article, obj_in: ArticleUpdate) -> Article:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete(db: Session, article_id: int):
        db_obj = db.query(Article).filter(Article.id == article_id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj
