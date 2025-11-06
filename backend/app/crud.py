from sqlalchemy.orm import Session
from . import models
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username==username).first()

def create_user(db: Session, username: str, password: str):
    password = password[:72]  # truncate to max bcrypt length
    hashed_password = pwd_context.hash(password)
    db_user = models.User(username=username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user