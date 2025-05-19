from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "shop"


urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation-page/', views.order_confirm, name='order_confirm'),
    path('product/<int:product_id>/review/', views.post_review, name='post_review'),
    path('review/<int:review_id>/reply/', views.post_reply, name='post_reply'),


]
