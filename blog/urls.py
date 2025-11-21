from django.urls import path

from . import views

app_name = 'blog'

# URLs docs
# https://docs.djangoproject.com/en/5.2/topics/http/urls/
urlpatterns = [
    path('', views.blog, name='home'),
    path('<int:post_id>/', views.post, name='post'),
    path('example/', views.example, name='example'),
]
