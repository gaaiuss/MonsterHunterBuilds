from django.core.exceptions import ValidationError
from django.forms import ImageField


def validate_png(image: ImageField) -> None:
    if not image.name.lower().endswith(".png"):  # type: ignore
        msg = "Image needs to be '.png'"
        raise ValidationError(msg)
