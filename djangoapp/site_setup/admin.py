from django.contrib import admin
from django.http import HttpRequest

from site_setup.models import MenuLink, SiteSetup


class MenuLinksInLine(admin.TabularInline):  # type: ignore
    model = MenuLink
    extra = 1


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):  # type: ignore
    list_display = "title", "description"
    inlines = (MenuLinksInLine,)

    def has_add_permission(self, request: HttpRequest) -> bool:
        print(request)
        return not SiteSetup.objects.exists()
