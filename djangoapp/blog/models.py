from django.db import models
from utils.rands import slugify_new


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True, default=None, null=True, blank=True, max_length=50
    )

    def save(self, *args, **kwargs) -> None:  # type: ignore # noqa: ANN002, ANN003
        if not self.slug:
            self.slug = slugify_new(self.name)
        return super().save(*args, **kwargs)  # type: ignore

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True, default=None, null=True, blank=True, max_length=50
    )

    def save(self, *args, **kwargs) -> None:  # type: ignore # noqa: ANN002, ANN003
        if not self.slug:
            self.slug = slugify_new(self.name)
        return super().save(*args, **kwargs)  # type: ignore

    def __str__(self) -> str:
        return self.name


class Page(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(
        unique=True, default="", null=False, blank=True, max_length=50
    )
    is_published = models.BooleanField(
        default=False, help_text="Mark this if you want to share your page publicly."
    )
    content = models.TextField()

    def save(self, *args, **kwargs) -> None:  # type: ignore # noqa: ANN002, ANN003
        if not self.slug:
            self.slug = slugify_new(self.title)
        return super().save(*args, **kwargs)  # type: ignore

    def __str__(self) -> str:
        return self.title
