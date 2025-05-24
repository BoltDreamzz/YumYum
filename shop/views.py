from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Payment, Order


import qrcode
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
from django.contrib.auth.decorators import login_required
from .models import Ingredient

# Create your views here.
from django.db.models import Q
from .models import Product, Category, Ingredient

def index(request):
    categories = Category.objects.all()
    ingredients = Ingredient.objects.all()

    # Get filter values
    search_query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')
    selected_ingredients = request.GET.getlist('ingredients')
    is_vegan = request.GET.get('is_vegan')
    is_gluten_free = request.GET.get('is_gluten_free')
    is_halal = request.GET.get('is_halal')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    sort_by = request.GET.get('sort_by')

    # Start with all products
    products = Product.objects.all()

    # Filter by search keyword
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Filter by category
    if selected_category:
        products = products.filter(category_id=selected_category)

    # Filter by ingredients
    if selected_ingredients:
        products = products.filter(ingredients__in=selected_ingredients).distinct()

    # Filter by checkboxes
    if is_vegan:
        products = products.filter(is_vegan=True)
    if is_gluten_free:
        products = products.filter(is_gluten_free=True)
    if is_halal:
        products = products.filter(is_halal=True)

    # Filter by price
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    # Sort
    if sort_by == "price_asc":
        products = products.order_by("price")
    elif sort_by == "price_desc":
        products = products.order_by("-price")
    elif sort_by == "newest":
        products = products.order_by("-created_at")  # Assuming your model has `created_at`
    elif sort_by == "name":
        products = products.order_by("name")
    elif sort_by == "random":
        products = products.order_by("?")

    return render(request, 'shop/index.html', {
        'categories': categories,
        'ingredients': ingredients,
        'products': products,
        'selected_category': selected_category,
        'selected_ingredients': selected_ingredients,
        'request': request,  # Pass request to use request.GET in the template
    })

from profiles.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/accounts/login/')
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    form = CartItemForm()

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Get product reviews and their replies
    reviewd = product.reviews.select_related('user').prefetch_related('replies__user')
    reviews = reviewd.order_by('-created')[:5]


    # Forms for review and reply
    review_form = ReviewForm()
    reply_form = ReviewReplyForm()

    # Related products
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'form': form,
        'reviews': reviews,
        'review_form': review_form,
        'reply_form': reply_form,
        'reviewd': reviewd,
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

# views.py
from django.conf import settings
from .cart import Cart  # or from your app if it's in another place

def cart_detail(request):
    cart = Cart(request)
    count = len(cart)

    total = cart.get_total_price()  # Assuming get_total_price is defined

    for item in cart:
        item['update_quantity_form'] = CartItemForm(initial={'quantity': item['quantity'], 'update': True})

    context = {
        'cart': cart,
        'count': count,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        'total_amount': int(total * 100),  # convert to kobo
    }

    return render(request, 'shop/cart_detail.html', context)


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



# views.py

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Review, ReviewReply
from .forms import ReviewForm, ReviewReplyForm
from django.template.loader import render_to_string


@login_required
# @csrf_exempt
# def post_review(request, product_id):
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.product_id = product_id
#             review.user = request.user
#             review.save()

#             html = render_to_string('partials/single_review.html', {'review': review}, request=request)
#             return JsonResponse({'message': 'Review posted successfully!', 'html': html}, status=200)
#         else:

#             return JsonResponse({'error': 'Invalid form data.'}, status=400)
#     return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required(login_url='/accounts/login/')
def post_review(request, product_id):

    
    if not request.user.is_authenticated:
        return JsonResponse({'login_required': True, 'error': 'You must be logged in to post a review.'})

    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        content = request.POST.get('content')
        rating = request.POST.get('rating')

        if not content or not rating:
            return JsonResponse({'error': 'Content and rating are required.'})

        review = Review.objects.create(
            product=product,
            user=user,
            content=content,
            rating=int(rating),
        )

    # Add a flag for just created reviews
        review.just_created = True
        review_html = render_to_string('partials/single_review.html', {'review': review}, request=request)


        return JsonResponse({
            'review_html': review_html,
            'message': 'Review posted successfully!',
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def post_reply(request, review_id):
    if request.method == 'POST':
        form = ReviewReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.review_id = review_id
            reply.user = request.user
            reply.save()

            html = render_to_string('partials/single_reply.html', {'reply': reply}, request=request)
            return JsonResponse({'message': 'Reply posted successfully!', 'html': html, 'review_id': review_id}, status=200)
        return JsonResponse({'error': 'Invalid form data.'}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)



def yum(request):
    return render(request, 'shop/yum.html')


from django.db.models import Q
from .models import Product

def product_search(request):
    queryset = Product.objects.filter(is_available=True)

    name = request.GET.get('name')
    category = request.GET.get('category')
    ingredients = request.GET.getlist('ingredients')
    is_vegan = request.GET.get('is_vegan')
    is_gluten_free = request.GET.get('is_gluten_free')
    is_halal = request.GET.get('is_halal')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    sort_by = request.GET.get('sort_by')

    if name:
        queryset = queryset.filter(name__icontains=name)

    if category:
        queryset = queryset.filter(category__id=category)

    if ingredients:
        queryset = queryset.filter(ingredients__id__in=ingredients).distinct()

    if is_vegan:
        queryset = queryset.filter(is_vegan=True)

    if is_gluten_free:
        queryset = queryset.filter(is_gluten_free=True)

    if is_halal:
        queryset = queryset.filter(is_halal=True)

    if price_min:
        queryset = queryset.filter(price__gte=price_min)

    if price_max:
        queryset = queryset.filter(price__lte=price_max)

    if sort_by == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort_by == 'price_desc':
        queryset = queryset.order_by('-price')
    elif sort_by == 'newest':
        queryset = queryset.order_by('-date_posted')
    elif sort_by == 'name':
        queryset = queryset.order_by('name')
    elif sort_by == 'random':
        queryset = queryset.order_by('?')

    if request.GET:
        request.session['last_search'] = request.GET.dict()

    filters = request.session.get('last_search', {})

    if request.htmx:
        return render(request, 'partials/product_list.html', {'products': queryset})
    return render(request, 'shop/product_search.html', {'products': queryset, 'filters': filters})

    

import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse
from .models import Payment, Order, OrderItem, Product, DeliveryAddress
from django.contrib.auth.decorators import login_required

@login_required
def initiate_payment(request):
    if request.method == 'POST':
        email = request.user.email
        amount = int(float(request.POST.get('amount')) * 100)  # convert to kobo

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "email": email,
            "amount": amount,
            "callback_url": request.build_absolute_uri('/verify-payment/')
        }

        response = requests.post('https://api.paystack.co/transaction/initialize', json=data, headers=headers)
        res_data = response.json()

        if res_data.get('status'):
            return redirect(res_data['data']['authorization_url'])
        else:
            messages.error(request, "Payment initialization failed.")
            return redirect('shop:cart_detail')  # Change to your cart view

    return render(request, 'shop/initiate_payment.html')


from django.core.mail import EmailMessage
from django.template.loader import render_to_string

@login_required
def verify_payment(request):
    reference = request.GET.get('reference')
    user = request.user
    cart = Cart(request)

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(url, headers=headers)
    res_data = response.json()

    if res_data['status'] and res_data['data']['status'] == 'success':
        total = res_data['data']['amount'] / 100

        # Create order
        order = Order.objects.create(user=user, total=total, status='completed')

        # Save each cart item to OrderItem
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )

        # Save payment
        Payment.objects.create(payment_reference=reference)

        # Clear cart
        cart.clear()

        # Send Order Confirmation Email to User using template
        user_subject = 'Order Confirmation'
        user_message = render_to_string('emails/order_confirmation.html', {
            'user': user,
            'order': order,
        })
        user_email = EmailMessage(
            subject=user_subject,
            body=user_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        user_email.content_subtype = 'html'
        user_email.send()

        # Send New Order Notification to Admin using template
        admin_subject = 'New Order Placed'
        admin_message = render_to_string('emails/new_order_notification.html', {
            'user': user,
            'order': order,
        })
        admin_email = EmailMessage(
            subject=admin_subject,
            body=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
        )
        admin_email.content_subtype = 'html'
        admin_email.send()

        messages.success(request, 'Payment verified. Order placed successfully!')
        return redirect('shop:order_detail', order_id=order.id)
    else:
        messages.error(request, 'Payment verification failed. Try again.')
        return redirect('shop:cart_detail')