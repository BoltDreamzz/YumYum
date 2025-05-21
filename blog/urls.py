from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('post/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('create/', views.blog_create, name='blog_create'),
    path('edit/<slug:slug>/', views.blog_edit, name='blog_edit'),
]
