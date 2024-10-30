# shop/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .cart import Cart

@receiver(user_logged_in)
def merge_carts_on_login(sender, request, user, **kwargs):
    session_cart = Cart(request)
    if session_cart.cart:
        # Here, you could write logic to merge with a user-based cart model if needed
        session_cart.clear()  # Clear session-based cart after login
