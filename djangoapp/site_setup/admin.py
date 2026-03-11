from django.contrib import admin
from django.http import HttpRequest

from site_setup.models import MenuLink, SiteSetup


@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):  # type: ignore
    list_display = "id", "text", "url_or_path"
    list_display_links = "id", "text", "url_or_path"
    search_fields = "id", "text", "url_or_path"


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):  # type: ignore
    list_display = "title", "description"

    def has_add_permission(self, request: HttpRequest) -> bool:
        print(request)
        return not SiteSetup.objects.exists()
