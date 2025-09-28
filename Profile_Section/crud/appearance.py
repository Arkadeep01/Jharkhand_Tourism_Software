from sqlalchemy.orm import Session
from Profile_Section.models.appearance import Appearance
from Profile_Section.schemas.appearance import AppearanceCreate, AppearanceUpdate

def get_appearance(db: Session, user_id: int):
    return db.query(Appearance).filter(Appearance.user_id == user_id).first()

def create_appearance(db: Session, user_id: int, appearance_create: AppearanceCreate):
    db_appearance = Appearance(
        user_id=user_id,
        theme=appearance_create.theme,
        palette_choice=appearance_create.palette_choice,
        font_family=appearance_create.font_family,
        extra_settings=appearance_create.extra_settings
    )
    db.add(db_appearance)
    db.commit()
    db.refresh(db_appearance)
    return db_appearance

def update_appearance(db: Session, user_id: int, appearance_update: AppearanceUpdate):
    appearance = get_appearance(db, user_id)
    if not appearance:
        return None
    for field, value in appearance_update.dict(exclude_unset=True).items():
        setattr(appearance, field, value)
    db.commit()
    db.refresh(appearance)
    return appearance
