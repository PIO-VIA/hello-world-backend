from sqlalchemy.orm import Session
from app.db.models.article import Article, ArticleStatus
from app.repositories.article_repository import ArticleRepository
from app.core.exceptions import PermissionDeniedError, NotFoundError

class ArticleService:
    @staticmethod
    def submit_for_review(db: Session, article_id: int, user_id: int) -> Article:
        article = ArticleRepository.get_by_id(db, article_id)
        if not article:
            raise NotFoundError(message="Article not found", code="ARTICLE_NOT_FOUND")
        if article.author_id != user_id:
            raise PermissionDeniedError(message="Only the author can submit the article", code="NOT_AUTHOR")
        
        from app.schemas.article import ArticleUpdate
        return ArticleRepository.update(db, db_obj=article, obj_in=ArticleUpdate(status=ArticleStatus.PENDING))

    @staticmethod
    def publish_article(db: Session, article_id: int) -> Article:
        article = ArticleRepository.get_by_id(db, article_id)
        if not article:
            raise NotFoundError(message="Article not found", code="ARTICLE_NOT_FOUND")
        
        from app.schemas.article import ArticleUpdate
        return ArticleRepository.update(db, db_obj=article, obj_in=ArticleUpdate(status=ArticleStatus.PUBLISHED))

    @staticmethod
    def reject_article(db: Session, article_id: int) -> Article:
        article = ArticleRepository.get_by_id(db, article_id)
        if not article:
            raise NotFoundError(message="Article not found", code="ARTICLE_NOT_FOUND")
        
        from app.schemas.article import ArticleUpdate
        return ArticleRepository.update(db, db_obj=article, obj_in=ArticleUpdate(status=ArticleStatus.DRAFT))
