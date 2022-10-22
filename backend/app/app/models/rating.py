from sqlalchemy import CheckConstraint, Column, ForeignKey, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Rating(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="ratings")
    stars = Column(
        SmallInteger,
        CheckConstraint("stars >= 0 and stars <= 5"),
        default=0,
        index=True,
    )
    # length of 11 based on highest logical version number
    model_version = Column(String(length=11), index=True)
