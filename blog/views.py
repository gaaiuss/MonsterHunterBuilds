from django.shortcuts import render


def blog(request):
    print('Blog')
    return render(request, 'blog/index.html')


def example(request):
    print('example')
    return render(request, 'blog/example.html')
