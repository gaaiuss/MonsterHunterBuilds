from django.shortcuts import render


def blog(request):
    print('Blog')

    context = {
        'text': 'Hello, blog page'
    }

    return render(
        request,
        'blog/index.html',
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
