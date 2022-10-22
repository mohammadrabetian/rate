from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.api.helpers.cache import get_model_version_from_cache_backend
from app.crud.base import CRUDBase
from app.models.rating import Rating
from app.schemas.rating import RatingCreate, RatingUpdate


class CRUDRating(CRUDBase[Rating, RatingCreate, RatingUpdate]):
    async def create_with_user(
        self, db: Session, *, obj_in: RatingCreate, user_id: UUID
    ) -> Rating:

        model_version = await get_model_version_from_cache_backend(
            source_lang=obj_in.source_lang, target_lang=obj_in.target_lang
        )
        db_obj = (
            db.query(self.model)
            .filter(Rating.user_id == user_id, Rating.model_version == model_version)
            .one_or_none()
        )
        if db_obj and db_obj.stars == obj_in.stars:
            return db_obj
        elif db_obj:
            db_obj.stars = obj_in.stars
        else:
            db_obj = self.model(
                stars=obj_in.stars, user_id=user_id, model_version=model_version
            )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_user(
        self, db: Session, *, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Rating]:
        return (
            db.query(self.model)
            .filter(Rating.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


rating = CRUDRating(Rating)
