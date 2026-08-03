"""QR code generation (PNG and SVG) — no hardcoded URLs, payload built from settings."""
import io

import qrcode
from qrcode.image.pil import PilImage
from qrcode.image.svg import SvgPathImage

from app.core.config import Settings

QR_BOX_SIZE = 12
QR_BORDER = 2


def public_emergency_url(settings: Settings, carecode: str) -> str:
    base = settings.public_url or f"http://localhost:8000"
    return f"{base}/e/{carecode}"


def generate_png(settings: Settings, carecode: str) -> bytes:
    payload = public_emergency_url(settings, carecode)
    qr = qrcode.QRCode(
        version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=QR_BOX_SIZE, border=QR_BORDER
    )
    qr.add_data(payload)
    qr.make(fit=True)
    img: PilImage = qr.make_image(fill_color="#0f172a", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_svg(settings: Settings, carecode: str) -> bytes:
    payload = public_emergency_url(settings, carecode)
    qr = qrcode.QRCode(
        version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=QR_BOX_SIZE, border=QR_BORDER
    )
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(image_factory=SvgPathImage)
    buf = io.BytesIO()
    img.save(buf)
    return buf.getvalue()
