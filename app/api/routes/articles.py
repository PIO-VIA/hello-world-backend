from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from app.api import deps
from app.db.models.user import User, UserRole
from app.db.models.article import ArticleStatus
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse
from app.repositories.article_repository import ArticleRepository
from app.services.article_service import ArticleService
from app.utils.responses import standard_response
from app.core.exceptions import PermissionDeniedError, NotFoundError

router = APIRouter()

@router.get("/")
def list_articles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[User] = Depends(deps.get_current_user), # Optional but we need it for unpublished
):
    """
    List articles. Published for everyone, all for Editors/Admins.
    """
    if current_user and current_user.role in [UserRole.EDITOR, UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        articles = ArticleRepository.list_all(db, skip=skip, limit=limit)
    else:
        articles = ArticleRepository.list_published(db, skip=skip, limit=limit)
        
    return standard_response(
        data=[ArticleResponse.from_orm(a) for a in articles],
        message="Articles retrieved",
        code="ARTICLES_RETRIEVED"
    )

@router.post("/", status_code=201)
def create_article(
    *,
    db: Session = Depends(deps.get_db),
    article_in: ArticleCreate,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Create a new article (Draft by default).
    """
    article = ArticleRepository.create(db, obj_in=article_in, author_id=current_user.id)
    return standard_response(
        data=ArticleResponse.from_orm(article),
        message="Article created as draft",
        code="ARTICLE_CREATED",
        status_code=201
    )

@router.get("/{article_id}")
def read_article(
    article_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Get article details.
    """
    article = ArticleRepository.get_by_id(db, article_id)
    if not article:
        raise NotFoundError(message="Article not found", code="ARTICLE_NOT_FOUND")
    return standard_response(
        data=ArticleResponse.from_orm(article),
        message="Article retrieved",
        code="ARTICLE_RETRIEVED"
    )

@router.put("/{article_id}")
def update_article(
    *,
    db: Session = Depends(deps.get_db),
    article_id: int,
    article_in: ArticleUpdate,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Update an article. Only author or Admin can update.
    """
    article = ArticleRepository.get_by_id(db, article_id)
    if not article:
        raise NotFoundError(message="Article not found", code="ARTICLE_NOT_FOUND")
    
    if article.author_id != current_user.id and current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise PermissionDeniedError(message="Not enough permissions", code="INSUFFICIENT_PERMISSIONS")
        
    article = ArticleRepository.update(db, db_obj=article, obj_in=article_in)
    return standard_response(
        data=ArticleResponse.from_orm(article),
        message="Article updated",
        code="ARTICLE_UPDATED"
    )

@router.post("/{article_id}/submit")
def submit_article(
    article_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Submit article for review.
    """
    article = ArticleService.submit_for_review(db, article_id, current_user.id)
    return standard_response(
        data=ArticleResponse.from_orm(article),
        message="Article submitted for review",
        code="ARTICLE_SUBMITTED"
    )

@router.post("/{article_id}/publish", dependencies=[Depends(deps.RoleChecker([UserRole.EDITOR, UserRole.ADMIN, UserRole.SUPER_ADMIN]))])
def publish_article(
    article_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Publish an article (Editor/Admin only).
    """
    article = ArticleService.publish_article(db, article_id)
    return standard_response(
        data=ArticleResponse.from_orm(article),
        message="Article published",
        code="ARTICLE_PUBLISHED"
    )

@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Delete an article.
    """
    article = ArticleRepository.get_by_id(db, article_id)
    if not article:
        raise NotFoundError(message="Article not found", code="ARTICLE_NOT_FOUND")
    
    if article.author_id != current_user.id and current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise PermissionDeniedError(message="Not enough permissions", code="INSUFFICIENT_PERMISSIONS")
        
    ArticleRepository.delete(db, article_id)
    return standard_response(message="Article deleted", code="ARTICLE_DELETED")
