from models import UserAppearance
from schemas import AppearanceUpdateSchema

def get_user_appearance(user_id: int):
    """Fetch user's appearance settings."""
    return UserAppearance.get(user_id=user_id)

def update_user_appearance(user_id: int, data: AppearanceUpdateSchema):
    """Update theme, language, or font for the user."""
    appearance = UserAppearance.get(user_id=user_id)
    if appearance:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(appearance, key, value)
        appearance.save()
    return appearance
