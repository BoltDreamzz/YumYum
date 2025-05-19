from django.contrib import admin
from .models import Category, Product, Review, DeliveryAddress, ReviewReply, Order, OrderItem, Payment

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(DeliveryAddress)
admin.site.register(Review)
admin.site.register(ReviewReply)
admin.site.register(Order)

admin.site.register(OrderItem)
admin.site.register(Payment)