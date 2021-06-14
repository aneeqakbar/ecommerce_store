from django.core.management.base import BaseCommand
from shop.models import Image, ImageAlbum, Product
from django.contrib.auth.models import User
import json,requests

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _get_data(self):
        response = requests.get('https://fakestoreapi.com/products?limit=1')
        return json.loads(response.text)

    def _create_tags(self):
        data = self._get_data()
        for product in data:
            image_album = ImageAlbum.objects.create()
            im = requests.get(product['image'], stream=True,)
            Image.objects.create(
                album = image_album,
                image =  im.content
            )
            product_instance = Product.objects.create(
                user = User.objects.get(pk=1),
                name = product['title'],
                price = product['price'],
                description = product['description'],
                album = image_album
            )
            product_instance.save()

    def handle(self, *args, **options):
        self._create_tags()
        self.stdout.write(self.style.SUCCESS('Successfully Popullated Database'))