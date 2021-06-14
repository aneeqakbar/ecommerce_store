import json
from user.models import Profile
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.urls.base import reverse
from shop.forms import AddProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.utils import timezone
from .models import Image,ImageAlbum, Orderitem, Payment,Product,Order
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from notifications.signals import notify
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

@method_decorator(login_required, name='dispatch')
class AddProductView(View):
    def get(self,*args, **kwargs):
        form = AddProductForm()
        context = {'form':form}
        return render(self.request,'add_product.html',context)
    def post(self,*args, **kwargs):
        form = AddProductForm(self.request.POST)
        if form.is_valid():
            
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            discount = form.cleaned_data['discount_price']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            
            product = Product.objects.create(
                user=self.request.user,
                name = name,
                price = price,
                discount_price = discount,
                description = description,
                category = category,
                album = ImageAlbum.objects.create()
                )
            
            images = self.request.FILES.getlist('images_files')
            
            if len(images) >= 12:
                images = images[0:12]
            for index,image in enumerate(images):
                img = Image.objects.create(
                    name = image.name,
                    image = image,
                    album = product.album,
                )
                if index == len(images)-1:
                    img.default = True
                    img.save()
            product.save()
        return HttpResponseRedirect(reverse('core:ProductView',kwargs={'pk':product.id}))


class order_summary(LoginRequiredMixin,View):
    def get(self,*args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered = False)
            print(order.products.all())
            context = {
                'cart':order,
                'STRIPE_PUBLIC_KEY' : settings.STRIPE_PUBLIC_KEY
                }
            return render(self.request,'cart.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,'You do not have any Order')
            return HttpResponseRedirect(reverse('core:HomeView'))


@login_required
def add_to_cart(request,pk):
    # product = Product.objects.get(pk=pk)
    product = get_object_or_404(Product,pk=pk)

    orderItem,created = Orderitem.objects.get_or_create(
        user=request.user,
        product = product,
        ordered = False)

    order_qs = Order.objects.filter(user=request.user,ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__pk = product.pk).exists():
            orderItem.quantity += 1
            orderItem.save()
            messages.info(request,'Quantity Added To the Cart')
            return HttpResponseRedirect(reverse('shop:order_summary'))
        else:
            orderItem.quantity = 1
            orderItem.save()
            order.products.add(orderItem)
            messages.info(request,'Item Added To the Cart')
            return HttpResponseRedirect(reverse('shop:order_summary'))
    else:
        current_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            ordered_date = current_date,
        )
        order.products.add(orderItem)
        order.save()
        messages.info(request,'Item Added To the Cart')
        return HttpResponseRedirect(reverse('shop:order_summary'))

def manage_quantity(req,action,pk):
    try:
        order_qs = Order.objects.filter(user=req.user,ordered = False)
        order = order_qs[0]
        orderItem = order.products.filter(product__pk = pk)[0]
        if action == 'r':
            if orderItem.quantity > 1:
                orderItem.quantity -= 1
                orderItem.save()
            else:
                orderItem.delete()
                # order.products.remove(orderItem)
                # order.save()
        elif action == 'a':
            orderItem.quantity += 1
            orderItem.save()
        return redirect('shop:order_summary')
    except ObjectDoesNotExist:
        raise Http404


#Check Out session creator
# class CreateCheckoutSessionView(View):
#     def post(self, request, *args, **kwargs):
#         # product_id = self.kwargs["pk"]
#         # order = Order.objects.get(user=request.user,ordered=False)
#         order = get_object_or_404(Order,user=request.user,ordered=False)
#         YOUR_DOMAIN = "http://127.0.0.1:8000"
#         price = order.get_total_price()
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price_data': {
#                         'currency': 'usd',
#                         'unit_amount': price*100,
#                         'product_data': {
#                             'name': order
#                         },
#                     },
#                     'quantity': 1,
#                 },
#             ],
#             metadata={
#                 "product_id": order.id
#             },
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/success/',
#             cancel_url=YOUR_DOMAIN + '/cancel/',
#         )
#         return JsonResponse({
#         'id': checkout_session.id
#         })

#Creates custom Payment Intent
class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            if request.user.profile.stripe_customer_id is not None:
                customer = stripe.Customer.retrieve(request.user.profile.stripe_customer_id)
            else:
                customer = stripe.Customer.create(
                    name = request.user.username,
                    email = req_json['email'],
                    phone = request.user.profile.mobile_number,
                    address = {
                        'country' : 'Pakistan',
                        'state' : 'Sindh',
                        'city' : 'Karachi',
                        'postal_code' : '478500',
                        'line1' : 'Orangi town,chisti nagar'
                        },
                    )
                request.user.profile.stripe_customer_id = customer.id
                request.user.profile.save()
            # product_id = self.kwargs["pk"]
            # product = Product.objects.get(id=product_id)
            order = get_object_or_404(Order,user=request.user,ordered=False)
            price = order.get_total_price() *100
            intent = stripe.PaymentIntent.create(
                amount=price,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "order_id": order.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({ 'error': str(e) })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]

        product = Product.objects.get(id=product_id)

        # TODO - send an email to the customer
    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']
        receinpt_url = intent['charges']['data'][0]['receipt_url']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)
        profile = Profile.objects.get(stripe_customer_id = stripe_customer_id)
        payment = Payment.objects.create(
            user=profile.user,
            stripe_charge = intent.id,
            ammount = intent.amount,
            )

        customer_email = stripe_customer['email']
        order_id = intent["metadata"]["order_id"]

        order = Order.objects.get(id=order_id)
        for orderItem in order.products.all():
            orderItem.ordered = True
            orderItem.save()
        order.ordered = True
        order.save()

        sender = order
        receiver = profile.user
        notify.send(sender, recipient=receiver, verb='Message', description=f'Your payment of ({intent.amount / 100})$ is Accepted!')
        # return redirect('core:HomeView')

        # send_mail(
        #     subject="Here is your product",
        #     message=f"Thanks for your purchase. The URL is {product.url}",
        #     recipient_list=[customer_email],
        #     from_email="your@email.com"
        # )
    # elif event["type"] == "charge.succeeded":
    #     intent = event['data']['object']
    #     print('charge.succeeded',intent)

    return HttpResponse(status=200)