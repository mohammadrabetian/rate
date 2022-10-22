import pytest
from sqlalchemy.orm import Session

from app import crud
from app.schemas.rating import RatingCreate, RatingUpdate
from app.tests.utils.user import create_random_user


@pytest.mark.asyncio
async def test_create_rating(db: Session) -> None:
    stars = 5
    rating_in = RatingCreate(stars=stars, source_lang="en", target_lang="de")
    user = create_random_user(db)
    rating = await crud.rating.create_with_user(
        db=db, obj_in=rating_in, user_id=user.id
    )
    assert rating.stars == stars
    assert rating.user_id == user.id


@pytest.mark.asyncio
async def test_get_rating(db: Session) -> None:
    stars = 5
    rating_in = RatingCreate(stars=stars, source_lang="en", target_lang="de")
    user = create_random_user(db)
    rating = await crud.rating.create_with_user(
        db=db, obj_in=rating_in, user_id=user.id
    )
    stored_rating = crud.rating.get(db=db, id=rating.id)
    assert stored_rating
    assert rating.id == stored_rating.id
    assert rating.model_version == stored_rating.model_version
    assert rating.stars == stored_rating.stars
    assert rating.user_id == stored_rating.user_id


@pytest.mark.asyncio
async def test_update_rating(db: Session) -> None:
    stars = 5
    rating_in = RatingCreate(stars=stars, source_lang="en", target_lang="de")
    user = create_random_user(db)
    rating = await crud.rating.create_with_user(
        db=db, obj_in=rating_in, user_id=user.id
    )
    stars = 3
    rating_update = RatingUpdate(stars=stars)
    rating2 = crud.rating.update(db=db, db_obj=rating, obj_in=rating_update)
    assert rating.id == rating2.id
    assert rating.model_version == rating2.model_version
    assert rating2.stars == stars
    assert rating.user_id == rating2.user_id


@pytest.mark.asyncio
async def test_delete_rating(db: Session) -> None:
    stars = 5
    rating_in = RatingCreate(stars=stars, source_lang="en", target_lang="de")
    user = create_random_user(db)
    rating = await crud.rating.create_with_user(
        db=db, obj_in=rating_in, user_id=user.id
    )
    rating2 = crud.rating.remove(db=db, id=rating.id)
    rating3 = crud.rating.get(db=db, id=rating.id)
    assert rating3 is None
    assert rating2.id == rating.id
    assert rating2.stars == stars
    assert rating2.user_id == user.id
