# type:ignore

from typing import Any

from django.contrib.auth.models import User
from django.db.models import Q, QuerySet
from django.http import Http404
from django.http.request import HttpRequest  # noqa: TC002
from django.http.response import HttpResponse  # noqa: TC002
from django.shortcuts import redirect, render
from django.views.generic import ListView

from blog.models import Page, Post

PER_PAGE = 9


class PostListView(ListView):
    template_name = "blog/pages/index.html"
    context_object_name = "posts"
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({"page_title": "Home - "})
        return context


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__(**kwargs)
        self._temp_context = {}

    def get(
        self,
        request: HttpRequest,
        *args: Any,  # noqa: ANN401
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        author_pk = self.kwargs.get("author_pk")
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404

        self._temp_context.update({"author_pk": author_pk, "user": user})

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        user = self._temp_context["user"]
        user_full_name = user.username

        if user.first_name:
            user_full_name = f"{user.first_name} {user.last_name}"

        page_title = f"{user_full_name}'s posts - "
        context.update({"page_title": page_title})
        return context

    def get_queryset(self) -> QuerySet[Any]:
        author_pk = self._temp_context["author_pk"]
        return super().get_queryset().filter(created_by__pk=author_pk)


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(category__slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_title = f"{self.object_list[0].category.name} - Category - "
        context.update({"page_title": page_title})
        return context


class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(tags__slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_title = f"{self.object_list[0].tags.first().name} - Tag - "
        context.update({"page_title": page_title})
        return context


class SearchListView(PostListView):
    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(**kwargs)
        self._search_value = ""

    def setup(self, request: HttpRequest, *args: Any, **kwargs: dict[str, Any]) -> None:  # noqa: ANN401
        self._search_value = request.GET.get("search", "").strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        search_value = self._search_value
        return (
            super()
            .get_queryset()
            .filter(
                Q(title__icontains=search_value)
                | Q(excerpt__icontains=search_value)
                | Q(content__icontains=search_value)
            )[:PER_PAGE]
        )

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        search_value = self._search_value
        context.update(
            {
                "page_title": f"{search_value[:30]} - Search - ",
                "search_value": search_value,
            }
        )
        return context

    def get(
        self,
        request: HttpRequest,
        *args: Any,  # noqa: ANN401
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        if self._search_value == "":
            return redirect("blog:index")
        return super().get(request, *args, **kwargs)


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

    page_title = f"{search_value[:30]} - Search - "

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": posts,
            "search_value": search_value,
            "page_title": page_title,
        },
    )


def page(request: HttpRequest, slug: str) -> HttpResponse:
    page_obj = Page.objects.filter(is_published=True).filter(slug=slug).first()

    if page_obj is None:
        raise Http404

    page_title = f"{page_obj.title} - Page - "

    return render(
        request, "blog/pages/page.html", {"page": page_obj, "page_title": page_title}
    )


def post(request: HttpRequest, slug: str) -> HttpResponse:
    post_obj = Post.objects.get_published().filter(slug=slug).first()

    if post_obj is None:
        raise Http404

    page_title = f"{post_obj.title} - Post - "

    return render(
        request,
        "blog/pages/post.html",
        {
            "post": post_obj,
            "page_title": page_title,
        },
    )
