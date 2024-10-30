from django.shortcuts import render

# Create your views here.
def errand_index(request):
    return render(request, 'errands/errand_index.html')