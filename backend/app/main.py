import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .database import Base, engine, get_db, SessionLocal
from .models import User, Course, Enrollment, Opportunity, Bookmark
from .schemas import Registration, Login, UserOut, TokenOut, CourseOut, OpportunityOut
from .auth import hasher, create_token, current_user
from .seed import seed

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        seed(db)
    yield

app = FastAPI(title="CampusConnect API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(","), allow_credentials=True, allow_methods=["GET", "POST", "DELETE"], allow_headers=["Authorization", "Content-Type"])

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/auth/register", response_model=TokenOut, status_code=201)
def register(data: Registration, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == str(data.email).lower())):
        raise HTTPException(409, "Email already registered")
    user = User(name=data.name.strip(), email=str(data.email).lower(), password_hash=hasher.hash(data.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Email already registered")
    db.refresh(user)
    return {"access_token": create_token(user.id)}

@app.post("/api/auth/login", response_model=TokenOut)
def login(data: Login, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == str(data.email).lower()))
    if not user or not hasher.verify(data.password, user.password_hash):
        raise HTTPException(401, "Incorrect email or password")
    return {"access_token": create_token(user.id)}

@app.get("/api/users/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user

@app.get("/api/courses", response_model=list[CourseOut])
def courses(search: str = Query("", max_length=100), department: str = "", db: Session = Depends(get_db)):
    q = select(Course)
    if search:
        q = q.where(Course.code.ilike(f"%{search}%") | Course.title.ilike(f"%{search}%"))
    if department:
        q = q.where(Course.department == department)
    items = db.scalars(q.order_by(Course.code)).all()
    counts = dict(db.execute(select(Enrollment.course_id, func.count()).group_by(Enrollment.course_id)).all())
    return [CourseOut.model_validate(c).model_copy(update={"enrolled": counts.get(c.id, 0)}) for c in items]

@app.get("/api/enrollments", response_model=list[int])
def my_enrollments(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return list(db.scalars(select(Enrollment.course_id).where(Enrollment.user_id == user.id)))

@app.post("/api/enrollments/{course_id}", status_code=201)
def enroll(course_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(404, "Course not found")
    if db.scalar(select(Enrollment.id).where(Enrollment.user_id == user.id, Enrollment.course_id == course_id)):
        raise HTTPException(409, "Already enrolled")
    # Lock course row on databases that support row-level locking to avoid capacity races.
    db.execute(select(Course).where(Course.id == course_id).with_for_update()).scalar_one()
    count = db.scalar(select(func.count()).select_from(Enrollment).where(Enrollment.course_id == course_id))
    if count >= course.capacity:
        raise HTTPException(409, "Course is full")
    db.add(Enrollment(user_id=user.id, course_id=course_id))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Already enrolled")
    return {"message": "Enrollment successful"}

@app.delete("/api/enrollments/{course_id}")
def unenroll(course_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    item = db.scalar(select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.course_id == course_id))
    if not item:
        raise HTTPException(404, "Enrollment not found")
    db.delete(item)
    db.commit()
    return {"message": "Enrollment removed"}

@app.get("/api/opportunities", response_model=list[OpportunityOut])
def opportunities(search: str = Query("", max_length=100), kind: str = "", db: Session = Depends(get_db)):
    q = select(Opportunity)
    if search:
        q = q.where(Opportunity.title.ilike(f"%{search}%") | Opportunity.organization.ilike(f"%{search}%"))
    if kind:
        q = q.where(Opportunity.kind == kind)
    return db.scalars(q.order_by(Opportunity.id)).all()

@app.get("/api/bookmarks", response_model=list[int])
def bookmarks(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return list(db.scalars(select(Bookmark.opportunity_id).where(Bookmark.user_id == user.id)))

@app.post("/api/bookmarks/{opportunity_id}", status_code=201)
def bookmark(opportunity_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if not db.get(Opportunity, opportunity_id):
        raise HTTPException(404, "Opportunity not found")
    if db.scalar(select(Bookmark.id).where(Bookmark.user_id == user.id, Bookmark.opportunity_id == opportunity_id)):
        raise HTTPException(409, "Already saved")
    db.add(Bookmark(user_id=user.id, opportunity_id=opportunity_id))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Already saved")
    return {"message": "Opportunity saved"}

@app.delete("/api/bookmarks/{opportunity_id}")
def remove_bookmark(opportunity_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    item = db.scalar(select(Bookmark).where(Bookmark.user_id == user.id, Bookmark.opportunity_id == opportunity_id))
    if not item:
        raise HTTPException(404, "Bookmark not found")
    db.delete(item)
    db.commit()
    return {"message": "Bookmark removed"}
