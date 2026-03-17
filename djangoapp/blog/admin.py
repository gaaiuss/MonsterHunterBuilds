from django.contrib import admin

from blog.models import Category, Page, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):  # type: ignore
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
class CategoryAdmin(admin.ModelAdmin):  # type: ignore
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
class PageAdmin(admin.ModelAdmin):  # type: ignore
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
