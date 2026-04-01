# type: ignore
from typing import Any, Self

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django_summernote.models import AbstractAttachment
from utils.images import resize_image
from utils.rands import slugify_new


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True, default=None, null=True, blank=True, max_length=50
    )

    def save(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        if not self.slug:
            self.slug = slugify_new(self.name)
        super().save(*args, **kwargs)

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

    def save(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        if not self.slug:
            self.slug = slugify_new(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Page(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(
        unique=True, default="", null=False, blank=True, max_length=50
    )
    is_published = models.BooleanField(
        default=False, help_text="Share your page publicly."
    )
    content = models.TextField()

    def save(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        if not self.slug:
            self.slug = slugify_new(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        if not self.is_published:
            return reverse("blog:index")

        return reverse("blog:page", args=(self.slug,))

    def __str__(self) -> str:
        return self.title


class PostManager(models.Manager):
    def get_published(self) -> Self:
        return self.filter(is_published=True).order_by("-pk")


class Post(models.Model):
    objects = PostManager()

    title = models.CharField(max_length=100)
    slug = models.SlugField(
        unique=True, default="", null=False, blank=True, max_length=50
    )
    excerpt = models.CharField(max_length=200)
    is_published = models.BooleanField(
        default=True, help_text="Share your post publicly."
    )
    content = models.TextField()
    cover = models.ImageField(upload_to="posts/%Y/%m/", blank=True, default="")
    cover_in_post_content = models.BooleanField(
        default=True, help_text="Show cover image in post content."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="post_created_by",
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="post_updated_by",
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        if not self.slug:
            self.slug = slugify_new(self.title)

        current_cover_name = str(self.cover.name) if self.cover else ""
        super().save(*args, **kwargs)

        if self.cover and current_cover_name != self.cover.name:
            resize_image(self.cover, 900, 70)

    def get_absolute_url(self) -> str:
        if not self.is_published:
            return reverse("blog:index")

        return reverse("blog:post", args=(self.slug,))

    def __str__(self) -> str:
        return self.title


class PostAttachment(AbstractAttachment):
    def save(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name) if self.file else ""
        super().save(*args, **kwargs)

        if self.file and current_file_name != self.file.name:
            resize_image(self.file, 900, 70)
