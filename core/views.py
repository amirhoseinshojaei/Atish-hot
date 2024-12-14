from django.shortcuts import render
from . models import Products, CustomerReview
# Create your views here.


def index(request):
    latest_products = Products.objects.order_by('-created_at')[:6]
    suggested_products = Products.objects.filter(is_suggestion=True)[:6]
    customer_reviews = CustomerReview.objects.order_by('-created_at')[:4]

    return render(request, 'core/index.html', {
        'latest_products': latest_products,
        'suggested_products': suggested_products,
        'customer_reviews': customer_reviews
    })


