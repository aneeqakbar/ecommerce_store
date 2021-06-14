from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from .choices import (CATEGORIES,LABEL)
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

def get_upload_path(instance, filename):
    model = instance.album.model.__class__._meta
    name = model.verbose_name_plural.replace(' ', '_')
    return f'{name}/images/{filename}'

class ImageAlbum(models.Model):
    def __str__(self):
        try:
            return self.model.name + ' (Album)'
        except ObjectDoesNotExist:
            return '--' + f"({self.pk})"
    def default(self):
        return self.images.filter(default=True).first()
    def thumbnails(self):
        return self.images.filter(width__lt=100, length_lt=100)

class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_upload_path)
    default = models.BooleanField(default=False)
    width = models.FloatField(default=100)
    length = models.FloatField(default=100)
    album = models.ForeignKey(ImageAlbum, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.album.model.name}({self.album.model.pk})"

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    price = models.FloatField()
    discount_price = models.FloatField(null=True,blank=True)
    category = models.CharField(choices=CATEGORIES,max_length=2)
    label = models.CharField(choices=LABEL,max_length=2,default='N')
    description = models.TextField()
    created_on = models.DateField(auto_now=True)
    album = models.OneToOneField(ImageAlbum, related_name='model', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('core:ProductView', kwargs={
            'pk': self.pk
        })

    def get_add_to_cart_url(self):
        return reverse('shop:add_to_cart', kwargs={
            'pk': self.pk
        })
        
    def get_remove_from_cart_url(self):
        return reverse("shop:remove_from_cart", kwargs={
            "pk": self.pk
        })


# ::::::::::::::::::::::::Payment Models:::::::::::::::::::::::::: #

class Orderitem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} Piece(s) of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_discount_item_percentage(self):
        if self.product.discount_price is not None:
            percentage = (self.get_amount_saved() / self.get_total_item_price()) * 100
            return round(percentage,2)
        return 0

    def get_discount_item_price(self):
        if self.product.discount_price is not None:
            return self.quantity * self.product.discount_price
        return self.quantity * self.product.price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='order')
    products = models.ManyToManyField(Orderitem)
    start_date = models.DateField(auto_now_add=True)
    ordered_date = models.DateField()
    ordered = models.BooleanField(default=False)

    def __str__(self,*args, **kwargs):
        return f'{self.user.username} {self.start_date}'

    def get_count(self,*args, **kwargs):
        return self.products.all().count()
        
    def get_total_price(self,*args, **kwargs):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price()
        return round(total)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
    stripe_charge = models.CharField(max_length=50)
    timestamp = models.TimeField(auto_now_add=True)
    ammount = models.FloatField()

    def __str__(self,*args, **kwargs):
        return f'{self.user.username} ({self.ammount}$)'