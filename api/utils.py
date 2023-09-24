from PIL import Image as PILImage
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature


def generate_thumbnail(image, height):
    aspect_ratio = image.width / image.height
    new_width = int(aspect_ratio * height)
    thumbnail = image.resize((new_width, height), PILImage.LANCZOS)
    return thumbnail


def generate_signed_url(path, expiration_seconds):
    signer = TimestampSigner()
    signed_path = signer.sign(path)
    return f"{path}?token={signed_path.split(':')[1]}"


def validate_signed_url(path, token, expiration_seconds):
    signer = TimestampSigner()
    try:
        signed_path = f"{path}:{token}"
        original = signer.unsign(signed_path, max_age=expiration_seconds)
        return True
    except (BadSignature, SignatureExpired):
        return False
