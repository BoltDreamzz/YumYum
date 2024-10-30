from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Payment, Order


import qrcode
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO


# Create your views here.
def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'shop/index.html', {
        'categories': categories,
        'products': products,
    })
    
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = CartItemForm()
    # Fetch related products, excluding the current product
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'form': form,
    })
    
    
# shop/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .cart import Cart
from django.contrib import messages


# shop/views.py
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CartItemForm
from django.http import JsonResponse

# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartItemForm(request.POST)
    
#     if form.is_valid():
#         quantity = form.cleaned_data['quantity']
#         update = form.cleaned_data['update']
#         cart.add(product=product, quantity=quantity, override_quantity=update)
#         messages.success(request, 'Added to cart')
        
        
    
#     # return redirect('shop:product_detail', product_id=product.id)
#     return redirect('shop:cart_detail')


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartItemForm(request.POST)
    
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        update = form.cleaned_data['update']
        
        # Add the item to the cart with specified quantity
        cart_item = cart.add(product=product, quantity=quantity, override_quantity=update)
        messages.success(request, 'Added to cart')

        # Check if the request is an AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Return the updated total price as JSON
            return JsonResponse({
                'total_price': cart_item.get_total_price()  # Assuming `get_total_price` is a method that returns item total price
            })
    
    # Redirect to the cart detail page for non-AJAX requests
    return redirect('shop:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, 'Removed from cart')
    return redirect('shop:product_detail', product_id=product.id)

# shop/views.py
from .forms import CartItemForm

def cart_detail(request):
    cart = Cart(request)
    count = len(cart)
    
    for item in cart:
        item['update_quantity_form'] = CartItemForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'shop/cart_detail.html', {'cart': cart, 'count': count,})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product
from .cart import Cart  # Make sure to import your Cart class
import json

@csrf_exempt
def update_cart(request, product_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        quantity = data.get('quantity')

        # Get the cart from the session
        cart = Cart(request)

        # Update the cart with the new quantity
        product = Product.objects.get(id=product_id)
        cart.add(product, quantity=quantity, override_quantity=True)

        # Calculate the new total price
        new_total_price = cart.get_total_price()

        return JsonResponse({'new_total_price': str(new_total_price)})  # Convert Decimal to string for JSON
    
    


from .forms import CheckoutForm, DeliveryAddressForm



# def checkout(request):
#     request.session.create() if not request.session.session_key else None

#     cart = Cart(request)
#     total_price = cart.get_total_price()
#     messages.success(request, 'Please make payments')
    
#     opay_account_number = "8111440535" 
#     palmpay_account_number = "8140413937"

#     # Generate QR code with account number
#     qr = qrcode.make(account_number)
#     qr_image = BytesIO()
#     qr.save(qr_image, format="PNG")
#     qr_image.seek(0)

#     if request.method == 'POST':
#         checkout_form = CheckoutForm(request.POST, request.FILES)
#         address_form = DeliveryAddressForm(request.POST)
#         if checkout_form.is_valid() and address_form.is_valid():
#             # Save the delivery address
#             delivery_address = address_form.save()

#             # Save the payment information
#             payment_reference = checkout_form.cleaned_data['payment_reference']
#             payment_screenshot = checkout_form.cleaned_data['payment_screenshot']
#             Payment.objects.create(
#                 user=request.user,
#                 payment_reference=payment_reference,
#                 payment_screenshot=payment_screenshot,
#             )

#             # Create an order associated with the delivery address
#             order = Order.objects.create(
#                 delivery_address=delivery_address,
#                 status='pending',
#                 total=total_price,
#                 # Add other fields like total_price or status if necessary
#             )

#             # Clear the cart after successful order creation
#             cart.clear()
#             messages.success(request, 'Order placed successfully. Await confirmation.')
#             return redirect('shop:cart_detail')
#     else:
#         checkout_form = CheckoutForm()
#         address_form = DeliveryAddressForm()

#     return render(request, 'shop/checkout.html', {
#         'cart': cart,
#         'total_price': total_price,
#         'checkout_form': checkout_form,
#         'address_form': address_form,
#         'opay_account_number': opay_account_number,
#         'palmpay_account_number': palmpay_account_number,
#     })
import base64


def checkout(request):
    request.session.create() if not request.session.session_key else None

    cart = Cart(request)
    total_price = cart.get_total_price()
    messages.success(request, 'Please make payments')

    # Define multiple accounts with their names and account numbers
    accounts = [
        {'name': 'Opay', 'number': "8111-440-535"},
        {'name': 'PalmPay', 'number': "8140-413-937"},
        {'name': 'UBA', 'number': "217-735-058"}  # Add more accounts as needed
    ]

    # Generate QR codes and add them to the account details
    for account in accounts:
        qr = qrcode.make(account['number'])
        qr_image = BytesIO()
        qr.save(qr_image, format="PNG")
        qr_image.seek(0)
        qr_base64 = base64.b64encode(qr_image.getvalue()).decode('utf-8')
        account['qr_code'] = qr_base64

    if request.method == 'POST':
        checkout_form = CheckoutForm(request.POST, request.FILES)
        address_form = DeliveryAddressForm(request.POST)
        if checkout_form.is_valid() and address_form.is_valid():
            delivery_address = address_form.save()
            payment_reference = checkout_form.cleaned_data['payment_reference']
            payment_screenshot = checkout_form.cleaned_data['payment_screenshot']
            Payment.objects.create(
                user=request.user,
                payment_reference=payment_reference,
                payment_screenshot=payment_screenshot,
            )

            order = Order.objects.create(
                delivery_address=delivery_address,
                status='pending',
                total=total_price,
            )

            cart.clear()
            messages.success(request, 'Order placed successfully. Await confirmation.')
            return redirect('shop:order_confirm')
    else:
        checkout_form = CheckoutForm()
        address_form = DeliveryAddressForm()

    return render(request, 'shop/checkout.html', {
        'cart': cart,
        'total_price': total_price,
        'checkout_form': checkout_form,
        'address_form': address_form,
        'accounts': accounts,
    })
    
    
def order_confirm(request):
    # messages.success(request, 'Order placed !')
    return render(request, 'shop/order_confirm.html')