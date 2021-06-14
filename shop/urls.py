from django.urls import path
from .views import (
    AddProductView,
    add_to_cart,
    manage_quantity,
    order_summary,
    # CreateCheckoutSessionView,
    StripeIntentView,
    # payment_completed,
    stripe_webhook,
)

app_name = 'shop'

urlpatterns = [
    path('add_product/',AddProductView.as_view(),name='AddProductView'),
    path('add_to_cart/<pk>/',add_to_cart,name='add_to_cart'),
    path('order_summary/',order_summary.as_view(),name='order_summary'),
    path('manage_quantity/<slug:action>/<pk>/',manage_quantity,name='manage_quantity'),
    path('create-payment-intent/', StripeIntentView.as_view(), name='create-payment-intent'),
    # path('payment_completed/', payment_completed.as_view(), name='payment_completed'),
    # path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
]
# C:\Users\Aneeq-PC\Downloads\Compressed\stripe_1.6.1_windows_x86_64\stripe.exe listen --forward-to localhost:8000/shop/webhooks/stripe/
