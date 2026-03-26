#type:ignore
from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from blog.models import Post

PER_PAGE = 9


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.get_published()
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/pages/index.html", {"page_obj": page_obj})


def page(request: HttpRequest) -> HttpResponse:
    return render(request, "blog/pages/page.html")


def post(request: HttpRequest) -> HttpResponse:
    return render(request, "blog/pages/post.html")
