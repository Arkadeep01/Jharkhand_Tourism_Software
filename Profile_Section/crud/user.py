from sqlalchemy.orm import Session
from passlib.context import CryptContext
from Profile_Section.models.user import User
from Profile_Section.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_create: UserCreate):
    hashed_pw = pwd_context.hash(user_create.password)
    db_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_pw,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        phone=user_create.phone,
        bio=user_create.bio,
        avatar_url=user_create.avatar_url,
        location=user_create.location,
        traveler_type=user_create.traveler_type,
        interests=user_create.interests,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = get_user(db, user_id)
    if not user:
        return None
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def set_avatar(db: Session, user_id: int, avatar_url: str):
    user = get_user(db, user_id)
    if not user:
        return None
    user.avatar
