from pathlib import Path
from typing import Any

from django.conf import settings
from PIL import Image


def resize_image(
    image_django: Any,  # noqa: ANN401
    new_width: int = 800,
    quality: int = 60,
) -> Image.Image:
    image_path = Path(settings.MEDIA_ROOT / image_django.name).resolve()  # type: ignore
    image_pillow = Image.open(image_path)
    original_width, original_height = image_pillow.size

    if original_width <= new_width:
        image_pillow.close()
        return image_pillow

    new_height = round(new_width * original_height / original_width)

    new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)

    new_image.save(
        image_path,
        optimize=True,
        quality=quality,
    )

    return new_image
