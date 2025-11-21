from typing import Any

from django.http import Http404, HttpRequest
from django.shortcuts import render

from blog.data import posts


def blog(request):
    print('Blog')

    context = {
        # 'text': 'Hello, blog page',
        'posts': posts
    }

    return render(
        request,
        'blog/index.html',
        context
    )


def post(request: HttpRequest, post_id: int):
    found_post: dict[str, Any] | None = None

    for post in posts:
        if post['id'] == post_id:
            found_post = post
            break

    if found_post is None:
        raise Http404('Post URL not found.')

    context = {
        # 'text': 'Hello, blog page',
        'post': found_post,
        'title': found_post['title'] + ' - '
    }

    return render(
        request,
        'blog/post.html',
        context
    )


def example(request):
    print('example')

    context = {
        'text': 'Hello, example page',
        'title': 'This is an example page - '
    }

    return render(
        request,
        'blog/example.html',
        context
    )
