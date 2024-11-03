from django.shortcuts import render, redirect

from .forms import CourierServiceForm
# Create your views here.
def errand_index(request):
    if request.method == "POST":
        form = CourierServiceForm(request.POST)
        if form.is_valid():
            form.save()  # Save form data directly to the Delivery model
            return redirect('errands:success')
    else:
        form = CourierServiceForm()
    
    return render(request, 'errands/errand_index.html', {'form': form})


def errand_page(request):
    if request.method == "POST":
        form = CourierServiceForm(request.POST)
        if form.is_valid():
            form.save()  # Save form data directly to the Delivery model
            return redirect('errands:success')
    else:
        form = CourierServiceForm()
    return render(request, 'errands/errand_page.html', {
        'form': form,
    })


def success(request):
    return render(request, 'errands/success.html')

from .forms import ShippingCalculatorForm

def shipping_calculator(request):
    total_cost = None
    if request.method == 'POST':
        form = ShippingCalculatorForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            total_cost = delivery.calculate_total_cost()
            # delivery.save()
            
            # You could save the delivery if desired with `delivery.save()`
    else:
        form = ShippingCalculatorForm()

    return render(request, 'errands/shipping_calculator.html', {'form': form, 'total_cost': total_cost})