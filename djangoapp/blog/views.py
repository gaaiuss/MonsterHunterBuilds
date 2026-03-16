from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "blog/pages/index.html")


def page(request: HttpRequest) -> HttpResponse:
    return render(request, "blog/pages/page.html")


def post(request: HttpRequest) -> HttpResponse:
    return render(request, "blog/pages/post.html")
