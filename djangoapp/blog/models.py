from django.contrib.auth.models import User
from django.db import models
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
        default=False, help_text="Share your page publicly."
    )
    content = models.TextField()

    def save(self, *args, **kwargs) -> None:  # type: ignore # noqa: ANN002, ANN003
        if not self.slug:
            self.slug = slugify_new(self.title)
        return super().save(*args, **kwargs)  # type: ignore

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
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
    # user.post_created_by.all  # noqa: ERA001
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="post_created_by",
    )
    updated_at = models.DateTimeField(auto_now=True)
    # user.post_updated_by.all  # noqa: ERA001
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
    tag = models.ManyToManyField(Tag, blank=True, default="")  # type: ignore

    def save(self, *args, **kwargs) -> None:  # type: ignore # noqa: ANN002, ANN003
        if not self.slug:
            self.slug = slugify_new(self.title)

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)  # type: ignore
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_image(self.cover, 900, 70)

        return super_save

    def __str__(self) -> str:
        return self.title


class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)  # type: ignore
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name

        if file_changed:
            resize_image(self.file, 900, 70)

        return super_save
