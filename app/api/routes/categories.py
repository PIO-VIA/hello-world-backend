from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.db.models.user import User, UserRole
from app.schemas.article import CategoryCreate, CategoryUpdate, CategoryResponse
from app.repositories.article_repository import CategoryRepository
from app.utils.responses import standard_response

router = APIRouter()

@router.get("/", response_model=None)
def list_categories(
    db: Session = Depends(deps.get_db),
):
    """
    List all categories.
    """
    categories = CategoryRepository.list(db)
    return standard_response(
        data=[CategoryResponse.from_orm(c) for c in categories],
        message="Categories retrieved",
        code="CATEGORIES_RETRIEVED"
    )

@router.post("/", dependencies=[Depends(deps.RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN]))])
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: CategoryCreate
):
    """
    Create a new category (Admin only).
    """
    category = CategoryRepository.create(db, obj_in=category_in)
    return standard_response(
        data=CategoryResponse.from_orm(category),
        message="Category created",
        code="CATEGORY_CREATED",
        status_code=201
    )

@router.put("/{category_id}", dependencies=[Depends(deps.RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN]))])
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    category_in: CategoryUpdate
):
    """
    Update a category (Admin only).
    """
    category = CategoryRepository.get_by_id(db, category_id)
    if not category:
        from app.core.exceptions import NotFoundError
        raise NotFoundError(message="Category not found", code="CATEGORY_NOT_FOUND")
    category = CategoryRepository.update(db, db_obj=category, obj_in=category_in)
    return standard_response(
        data=CategoryResponse.from_orm(category),
        message="Category updated",
        code="CATEGORY_UPDATED"
    )

@router.delete("/{category_id}", dependencies=[Depends(deps.RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN]))])
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
):
    """
    Delete a category (Admin only).
    """
    CategoryRepository.delete(db, category_id)
    return standard_response(
        message="Category deleted",
        code="CATEGORY_DELETED"
    )
