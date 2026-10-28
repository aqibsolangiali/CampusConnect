from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(24), unique=True)
    title: Mapped[str] = mapped_column(String(150))
    department: Mapped[str] = mapped_column(String(70))
    credits: Mapped[int] = mapped_column(default=3)
    capacity: Mapped[int] = mapped_column(default=25)
    instructor: Mapped[str] = mapped_column(String(120))
    schedule: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(800))

class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (UniqueConstraint("user_id", "course_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))

class Opportunity(Base):
    __tablename__ = "opportunities"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(160))
    organization: Mapped[str] = mapped_column(String(120))
    kind: Mapped[str] = mapped_column(String(60))
    location: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(700))
    url: Mapped[str] = mapped_column(String(500), default="")

class Bookmark(Base):
    __tablename__ = "bookmarks"
    __table_args__ = (UniqueConstraint("user_id", "opportunity_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id"))
