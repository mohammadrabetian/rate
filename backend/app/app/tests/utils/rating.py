from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.rating import RatingCreate
from app.tests.utils.user import create_random_user


def create_random_rating(
    db: Session, *, user_id: Optional[UUID] = None
) -> models.Rating:
    if user_id is None:
        user = create_random_user(db)
        user_id = user.id
    obj_in = {"stars": 5, "model_version": "1.2.3"}
    return crud.rating.create(db=db, obj_in=obj_in, user_id=user_id)
