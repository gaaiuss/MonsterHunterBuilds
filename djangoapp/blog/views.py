# type:ignore

from django.core.paginator import Paginator
from django.db.models import Q
from django.http.request import HttpRequest  # noqa: TC002
from django.http.response import HttpResponse  # noqa: TC002
from django.shortcuts import render

from blog.models import Post

PER_PAGE = 9


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.get_published()
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/pages/index.html", {"page_obj": page_obj})


def created_by(request: HttpRequest, author_pk: int) -> HttpResponse:
    posts = Post.objects.get_published().filter(created_by__pk=author_pk)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/pages/index.html", {"page_obj": page_obj})


def category(request: HttpRequest, slug: str) -> HttpResponse:
    posts = Post.objects.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/pages/index.html", {"page_obj": page_obj})


def tag(request: HttpRequest, slug: str) -> HttpResponse:
    posts = Post.objects.get_published().filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/pages/index.html", {"page_obj": page_obj})


def search(request: HttpRequest) -> HttpResponse:
    search_value = request.GET.get("search", "").strip()

    posts = Post.objects.get_published().filter(
        # Title contains search value OR
        # Excerpt contains search value OR
        # Content contains search value
        Q(title__icontains=search_value)
        | Q(excerpt__icontains=search_value)
        | Q(content__icontains=search_value)
    )[:PER_PAGE]

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": posts,
            "search_value": search_value,
        },
    )


def page(request: HttpRequest, slug: str) -> HttpResponse:
    print(slug)
    return render(request, "blog/pages/page.html")


def post(request: HttpRequest, slug: str) -> HttpResponse:
    post = Post.objects.get_published().filter(slug=slug).first()
    return render(
        request,
        "blog/pages/post.html",
        {
            "post": post,
        },
    )
