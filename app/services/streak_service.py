from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.repositories.interaction_repository import InteractionRepository
from app.schemas.interaction import StreakResponse

class StreakService:
    @staticmethod
    def update_streak(db: Session, user_id: int) -> StreakResponse:
        streak = InteractionRepository.get_streak(db, user_id)
        now = datetime.utcnow()
        
        if not streak:
            # First time login
            new_streak = InteractionRepository.upsert_streak(db, user_id, 1, now)
            return StreakResponse.from_orm(new_streak)
        
        last_login = streak.last_login
        diff = now.date() - last_login.date()
        
        if diff.days == 1:
            # Consecutive day
            updated_streak = InteractionRepository.upsert_streak(db, user_id, streak.count + 1, now)
        elif diff.days > 1:
            # Streak broken
            updated_streak = InteractionRepository.upsert_streak(db, user_id, 1, now)
        else:
            # Same day login, do nothing or update time
            updated_streak = streak
            
        return StreakResponse.from_orm(updated_streak)
