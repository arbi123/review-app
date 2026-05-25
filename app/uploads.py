import uuid
from pathlib import Path

from flask import current_app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload(file, subfolder: str) -> str | None:
    if not file or not file.filename:
        return None
    if not allowed_file(file.filename):
        return None

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    upload_root = Path(current_app.root_path) / "static" / "uploads" / subfolder
    upload_root.mkdir(parents=True, exist_ok=True)
    filepath = upload_root / filename
    file.save(filepath)
    return f"uploads/{subfolder}/{filename}"


def validate_image_upload(file) -> str | None:
    if not file or not file.filename:
        return None
    if not allowed_file(file.filename):
        return "Image must be PNG, JPG, JPEG, GIF, or WEBP."
    return None
