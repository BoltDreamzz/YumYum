from django.contrib import admin
from django.urls import path, include
from . import views


app_name = "errands"

urlpatterns = [
    path('', views.errand_index, name='errand_index'),
    # path('', include('shop.urls')),
    # path('errands', include('errands.urls')),
]
