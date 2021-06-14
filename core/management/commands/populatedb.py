from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from shop.models import Product

class Command(BaseCommand):
    help = 'Populates the database. Deletes old entries'

    def handle(self, *args, **options):
        print("Deleting old entries...")
        Product.objects.all().delete()
        print("Populating...")
        for i in range(100):
            Product.objects.create(
                user = User.objects.all().first(),
                name=str(i),
                price=i,
                category='TB',
                description = 'Auto Populated',
                )
        print("Done.")