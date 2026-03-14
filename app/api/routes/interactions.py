from typing import List
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.api import deps
from app.db.models.user import User, UserRole
from app.schemas.interaction import CommentCreate, CommentResponse, LikeResponse, StreakResponse, RewardResponse
from app.repositories.interaction_repository import InteractionRepository
from app.services.streak_service import StreakService
from app.services.reward_service import RewardService
from app.utils.responses import standard_response
from app.core.exceptions import PermissionDeniedError, NotFoundError

router = APIRouter()

# Comments
@router.post("/comments", status_code=201)
def add_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_in: CommentCreate,
    current_user: User = Depends(deps.get_current_user)
):
    comment = InteractionRepository.create_comment(db, obj_in=comment_in, user_id=current_user.id)
    return standard_response(data=CommentResponse.from_orm(comment), message="Comment added", status_code=201)

@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    comment = InteractionRepository.get_comment(db, comment_id)
    if not comment:
        raise NotFoundError(message="Comment not found", code="COMMENT_NOT_FOUND")
    if comment.user_id != current_user.id and current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise PermissionDeniedError(message="Not enough permissions", code="INSUFFICIENT_PERMISSIONS")
    InteractionRepository.delete_comment(db, comment_id)
    return standard_response(message="Comment deleted")

@router.post("/comments/{comment_id}/report")
def report_comment(
    comment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    comment = InteractionRepository.report_comment(db, comment_id)
    if not comment:
        raise NotFoundError(message="Comment not found", code="COMMENT_NOT_FOUND")
    return standard_response(message="Comment reported")

# Likes
@router.post("/articles/{article_id}/like")
def like_article(
    article_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    like = InteractionRepository.get_like(db, user_id=current_user.id, article_id=article_id)
    if like:
        return standard_response(message="Already liked", code="ALREADY_LIKED")
    like = InteractionRepository.create_like(db, user_id=current_user.id, article_id=article_id)
    return standard_response(data=LikeResponse.from_orm(like), message="Article liked")

@router.delete("/articles/{article_id}/like")
def unlike_article(
    article_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    InteractionRepository.delete_like(db, user_id=current_user.id, article_id=article_id)
    return standard_response(message="Like removed")

# Streaks
@router.post("/streaks/validate")
def validate_streak(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    streak = StreakService.update_streak(db, current_user.id)
    return standard_response(data=streak.model_dump(), message="Streak validated")

# Rewards
@router.post("/rewards/claim")
def claim_reward(
    qr_code_data: str = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    reward = RewardService.claim_reward(db, qr_code_data, current_user.id)
    return standard_response(data=reward.model_dump(), message="Reward claimed")

@router.post("/rewards/generate", dependencies=[Depends(deps.RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN]))])
def generate_reward(
    name: str = Body(...),
    description: str = Body(None),
    db: Session = Depends(deps.get_db)
):
    reward = RewardService.generate_reward(db, name, description)
    return standard_response(data=reward.model_dump(), message="Reward generated", status_code=201)
