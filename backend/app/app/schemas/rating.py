from uuid import UUID

from pydantic import BaseModel, validator


# Shared properties
class RatingBase(BaseModel):
    stars: int

    @validator("stars")
    def stars_between_zero_and_five(cls, v):
        """Apart from application level validation, DB level validation is also present."""
        assert 0 <= v <= 5, "must be between 0 and 5"
        return v


# Properties to receive on item creation
class RatingCreate(RatingBase):
    source_lang: str
    target_lang: str


# Properties to receive on item update
class RatingUpdate(RatingBase):
    ...


# Properties shared by models stored in DB
class RatingInDBBase(RatingBase):
    id: UUID
    user_id: UUID
    model_version: str

    class Config:
        orm_mode = True


# Properties to return to client
class Rating(RatingInDBBase):
    ...


# Properties properties stored in DB
class RatingInDB(RatingInDBBase):
    ...


class ModelVersion(BaseModel):
    version: str
