# type: ignore

from django.contrib import admin
from django.forms import ModelForm  # noqa: TC002
from django.http import HttpRequest  # noqa: TC002
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin

from blog.models import Category, Page, Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    list_display_links = ("name",)
    search_fields = (
        "id",
        "name",
        "slug",
    )
    list_per_page = 10
    ordering = ("-id",)
    prepopulated_fields = {"slug": ("name",)}  # noqa: RUF012


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    list_display_links = ("name",)
    search_fields = (
        "id",
        "name",
        "slug",
    )
    list_per_page = 10
    ordering = ("-id",)
    prepopulated_fields = {"slug": ("name",)}  # noqa: RUF012


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = (
        "id",
        "title",
        "is_published",
    )
    list_display_links = ("title",)
    search_fields = (
        "id",
        "title",
        "slug",
        "content",
    )
    list_per_page = 10
    ordering = ("-id",)
    prepopulated_fields = {"slug": ("title",)}  # noqa: RUF012


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = (
        "id",
        "title",
        "is_published",
        "created_by",
    )
    list_display_links = ("title",)
    search_fields = (
        "id",
        "title",
        "slug",
        "excerpt",
        "content",
    )
    list_per_page = 10
    list_filter = (
        "category",
        "is_published",
    )
    list_editable = ("is_published",)
    ordering = ("-id",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "link",
    )
    prepopulated_fields = {"slug": ("title",)}  # noqa: RUF012
    autocomplete_fields = (
        "tags",
        "category",
    )

    def link(self, obj: Post) -> str:
        if not obj.pk:
            return "-"

        post_url = obj.get_absolute_url()
        return mark_safe(f'<a target="_blank" href="{post_url}">See post</a>')  # noqa: S308

    def save_model(
        self,
        request: HttpRequest,
        obj: object,
        form: ModelForm,
        change: bool,  # noqa: FBT001
    ) -> None:
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user

        obj.save()
