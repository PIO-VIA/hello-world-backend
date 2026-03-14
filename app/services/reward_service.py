import uuid
from sqlalchemy.orm import Session
from app.repositories.interaction_repository import InteractionRepository
from app.schemas.interaction import RewardCreate, RewardResponse
from app.core.exceptions import NotFoundError, AppException

class RewardService:
    @staticmethod
    def generate_reward(db: Session, name: str, description: str = None) -> RewardResponse:
        qr_data = str(uuid.uuid4())
        reward_in = RewardCreate(name=name, description=description, qr_code_data=qr_data)
        reward = InteractionRepository.create_reward(db, reward_in)
        return RewardResponse.from_orm(reward)

    @staticmethod
    def claim_reward(db: Session, qr_code_data: str, user_id: int) -> RewardResponse:
        reward = InteractionRepository.get_reward_by_qr(db, qr_code_data)
        if not reward:
            raise NotFoundError(message="Reward not found", code="REWARD_NOT_FOUND")
        if reward.is_claimed:
            raise AppException(message="Reward already claimed", code="REWARD_CLAIMED")
            
        reward = InteractionRepository.claim_reward(db, reward, user_id)
        return RewardResponse.from_orm(reward)
