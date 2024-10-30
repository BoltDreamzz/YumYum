# shop/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_cart_reminder():
    users_with_carts = User.objects.filter(cart__isnull=False).distinct()
    for user in users_with_carts:
        if user.cart.items.exists():  # Modify based on actual cart model structure
            send_mail(
                'Complete Your Purchase!',
                'You have items left in your cart. Complete your purchase now!',
                'shop@example.com',
                [user.email],
                fail_silently=False,
            )
