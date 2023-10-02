from django.shortcuts import render
from .models import Product
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe
import json
from django.urls import reverse

def index(request):

    pr = Product.objects.all()
    context = {'pr': pr}
    return render(request, 'myapp/index.html', context)

def detail(request, id):
    p = Product.objects.get(id=id)
    spk = settings.STRIPE_PUBLISHABLE_KEY
    context = {'p': p, 'spk': spk}
    return render(request,'myapp/detail.html', context )

@csrf_exempt
def create_checkout_session(request, id):
    request_data = json.load(request.body)
    product = Product.objects.get(id=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = request_data['email'],
        payment_method_types = ['card'],
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': int(product.price *100)

                },
                'quantity': 1,

            }
        ],
        mode='payment',
        success_url = request.build_absolute_uri(reverse('success')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse('failed')),
    )










