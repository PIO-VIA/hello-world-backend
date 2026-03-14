from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.interaction import Comment, Like, Streak, Reward
from app.schemas.interaction import CommentCreate, RewardCreate
from datetime import datetime, timedelta

class InteractionRepository:
    # Comments
    @staticmethod
    def create_comment(db: Session, obj_in: CommentCreate, user_id: int) -> Comment:
        db_obj = Comment(**obj_in.model_dump(), user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get_comment(db: Session, comment_id: int) -> Optional[Comment]:
        return db.query(Comment).filter(Comment.id == comment_id).first()

    @staticmethod
    def delete_comment(db: Session, comment_id: int):
        db_obj = db.query(Comment).filter(Comment.id == comment_id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

    @staticmethod
    def report_comment(db: Session, comment_id: int) -> Optional[Comment]:
        db_obj = db.query(Comment).filter(Comment.id == comment_id).first()
        if db_obj:
            db_obj.is_reported = True
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    # Likes
    @staticmethod
    def get_like(db: Session, user_id: int, article_id: int) -> Optional[Like]:
        return db.query(Like).filter(Like.user_id == user_id, Like.article_id == article_id).first()

    @staticmethod
    def create_like(db: Session, user_id: int, article_id: int) -> Like:
        db_obj = Like(user_id=user_id, article_id=article_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete_like(db: Session, user_id: int, article_id: int):
        db_obj = db.query(Like).filter(Like.user_id == user_id, Like.article_id == article_id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

    # Streaks
    @staticmethod
    def get_streak(db: Session, user_id: int) -> Optional[Streak]:
        return db.query(Streak).filter(Streak.user_id == user_id).first()

    @staticmethod
    def upsert_streak(db: Session, user_id: int, count: int, last_login: datetime) -> Streak:
        streak = db.query(Streak).filter(Streak.user_id == user_id).first()
        if streak:
            streak.count = count
            streak.last_login = last_login
        else:
            streak = Streak(user_id=user_id, count=count, last_login=last_login)
        db.add(streak)
        db.commit()
        db.refresh(streak)
        return streak

    # Rewards
    @staticmethod
    def create_reward(db: Session, obj_in: RewardCreate) -> Reward:
        db_obj = Reward(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get_reward_by_qr(db: Session, qr_code_data: str) -> Optional[Reward]:
        return db.query(Reward).filter(Reward.qr_code_data == qr_code_data).first()

    @staticmethod
    def claim_reward(db: Session, db_obj: Reward, user_id: int) -> Reward:
        db_obj.user_id = user_id
        db_obj.is_claimed = True
        db_obj.claimed_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
