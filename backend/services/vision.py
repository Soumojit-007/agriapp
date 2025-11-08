import imghdr
import base64

def to_base64(file_bytes: bytes) -> str:
    if not file_bytes:
        raise ValueError("No bytes provided for Base64 conversion.")
    img_type = imghdr.what(None, file_bytes) or "jpeg"
    return f"data:image/{img_type};base64," + base64.b64encode(file_bytes).decode("utf-8")
