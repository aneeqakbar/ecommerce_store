import os
from django.db.models.signals import pre_save,post_save
from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from django.dispatch.dispatcher import receiver
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
# def get_upload_path(instance, filename):
#     return os.path.join('uploads', "user_%d" % instance.user.id, filename)

PROVINCES = (
    ('S','Sindh'),
    ('P','Punjab'),
    ('B','Balochistan'),
    ('K','Khyber PakhtunKhwa'),
    ('A','Azad Kashmir'),
)


def path_and_rename(instance, filename):
    ext = filename.split('.')[-1]
    user_id = "user_%d" % instance.user.id
    # set filename as random string
    random_id = "rid_%s" % (uuid4().hex,)
    filename = '{}.u{}.{}'.format(random_id,instance.user.id, ext)
    # return the whole path to the file
    return os.path.join('uploads', user_id, filename)

class Address(models.Model):
    country = CountryField(multiple=False,blank=False,max_length=3)
    province = models.CharField(max_length=3,choices=PROVINCES,blank=False)
    city = models.CharField(max_length=200,blank=False)
    street_address = models.CharField(max_length=100,blank=True)
    zip = models.CharField(max_length=100,blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(upload_to=path_and_rename, height_field=None, width_field=None,null=True)
    about_me = models.TextField(blank=True,null=True)
    mobile_number = PhoneNumberField()
    address = models.OneToOneField(Address, related_name='profile',null=True, blank=True,on_delete=models.SET_NULL)
    stripe_customer_id = models.CharField(max_length=100,default=None,null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User, dispatch_uid="Create-User-Profile")
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    # post_save provides 'created' arg and pre_save don't