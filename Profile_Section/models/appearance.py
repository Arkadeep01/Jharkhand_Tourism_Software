from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from Profile_Section.db.base import Base


class Appearance(Base):
    __tablename__ = "appearances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)

    # Basic theme mode
    theme = Column(String(50), default="light")  # light / dark

    # Palette selection
    palette_choice = Column(String(50), default="default")
    # Store the actual colors (hex values) so frontend can apply them directly
    palette_colors = Column(JSON, default={
        "light": {
            "blue_ocean": [
                "#03045e", "#023e8a", "#0077b6", "#0096c7", "#00b4d8", 
                "#48cae4", "#90e0ef", "#ade8f4", "#caf0f8"
            ],
            "green_nature": [
                "#d8f3dc", "#b7e4c7", "#95d5b2", "#74c69d", "#52b788",
                "#40916c", "#2d6a4f", "#1b4332", "#081c15"
            ],
            "warm_earth": [
                "#ffedd8", "#f3d5b5", "#e7bc91", "#d4a276", "#bc8a5f",
                "#a47148", "#8b5e34", "#6f4518", "#603808", "#583101"
            ],
        },
        "dark": {
            "purple_glow": [
                "#10002b", "#240046", "#3c096c", "#5a189a", "#7b2cbf",
                "#9d4edd", "#c77dff", "#e0aaff"
            ],
            "teal_ocean": [
                "#014d4e", "#016365", "#027779", "#028a8d", "#029ea1"
            ],
            "neutral_grey": [
                "#121212", "#2e2e2e", "#424242", "#575757", "#707070",
                "#8c8c8c", "#ababab", "#bdbdbd", "#d6d8dc", "#ebebeb"
            ],
        }
    })

    # Font customization
    font_family = Column(String(100), default="Noto Sans")
    available_fonts = Column(JSON, default={
        "dancing_script": '"Dancing Script", cursive',
        "noto_serif_kannada": '"Noto Serif Kannada", serif',
        "rubik_wet_paint": '"Rubik Wet Paint", system-ui',
        "gloria_hallelujah": '"Gloria Hallelujah", cursive',
        "tiro_devanagari": '"Tiro Devanagari Hindi", serif',
        "noto_sans_tamil": '"Noto Sans Tamil", sans-serif',
        "noto_sans": '"Noto Sans", sans-serif'
    })

    # Extra settings for flexibility (line spacing, contrast, etc.)
    extra_settings = Column(JSON, default={})

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
