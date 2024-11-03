from django.contrib import admin
from django.urls import path, include
from . import views


app_name = "errands"

urlpatterns = [
    path('', views.errand_index, name='errand_index'),
    path('success/', views.success, name='success'),  # Success page URL
    path('errand/', views.errand_page, name='errand_page'),

    path('shipping-calculator/', views.shipping_calculator, name='shipping_calculator'),

    # path('', include('shop.urls')),
    # path('errands', include('errands.urls')),
]
