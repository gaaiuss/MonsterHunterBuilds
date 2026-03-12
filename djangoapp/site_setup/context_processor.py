from django.http import HttpRequest

from site_setup.models import SiteSetup


def site_setup(request: HttpRequest) -> dict[str, SiteSetup | None]:
    setup = SiteSetup.objects.order_by("-id").first()

    return {"site_setup": setup}
