from datetime import datetime, timezone
from enum import StrEnum

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.core.database import Base


class UserType(StrEnum):
    pupil = "pupil"
    teacher = "teacher"
    manager = "manager"


class ClassLetter(StrEnum):
    A = "A"
    B = "Б"
    V = "В"
    G = "Г"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[str] = mapped_column(Text, nullable=True)
    date_entered: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    date_updated: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    user_type: Mapped[UserType] = mapped_column(
        Enum(UserType), nullable=False, default=UserType.pupil
    )

    scores: Mapped[list["Score"]] = relationship("Score", back_populates="user")
    pupil: Mapped["Pupil"] = relationship("Pupil", back_populates="user", uselist=False)
    __mapper_args__ = {
        "polymorphic_identity": "user",
    }


class Pupil(User):
    __tablename__ = "pupils"
    __table_args__ = (
        CheckConstraint(
            "class_number >= 1 AND class_number <= 11", name="class_number_range"
        ),
    )
    __mapper_args__ = {
        "polymorphic_identity": "pupil",
    }

    # id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, primary_key=True
    )
    date_of_birth: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    class_number: Mapped[Integer] = mapped_column(Integer, nullable=True)
    class_letter: Mapped[ClassLetter] = mapped_column(
        Enum(ClassLetter, values_callable=lambda x: [e.value for e in x]), nullable=True
    )
    user: Mapped["User"] = relationship("User", back_populates="pupil")
