from django.contrib import admin
from shop.models import Image, ImageAlbum, Order, Orderitem, Payment, Product

# Register your models here.

admin.site.register(Product)
admin.site.register(Image)
admin.site.register(ImageAlbum)
admin.site.register(Orderitem)
admin.site.register(Order)
admin.site.register(Payment)