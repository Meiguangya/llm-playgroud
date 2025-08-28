# app/crud/user.py
from sqlalchemy.orm import Session
from app import models, schemas
from app.core.security import hash_password


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user_in: schemas.UserCreate):
    hashed_password = hash_password(user_in.password)
    db_user = models.User(
        username=user_in.username,
        hashed_password=hashed_password,
        email=user_in.email,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user