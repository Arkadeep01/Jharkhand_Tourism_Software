import os
from fastapi import UploadFile
from uuid import uuid4

UPLOAD_DIR = "uploads/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def upload_avatar(file: UploadFile, user_id: int) -> str:
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise ValueError("Invalid file type. Only JPEG, PNG, WEBP allowed.")

    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    if file_size > MAX_FILE_SIZE:
        raise ValueError("File too large. Max 5MB allowed.")
    file.file.seek(0)

    filename = f"{user_id}_{uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Return relative/public URL for frontend
    return f"/{UPLOAD_DIR}/{filename}"
