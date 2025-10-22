from django.shortcuts import render


def home(request):
    print('Home')

    context = {
        'text': 'Hello, home page'
    }

    return render(
        request,
        'home/index.html',
        context
    )
