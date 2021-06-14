# Generated by Django 3.1.1 on 2021-05-25 02:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shop.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('discount_price', models.FloatField(blank=True, null=True)),
                ('category', models.CharField(choices=[('Mobiles', (('TB', 'Tablets'), ('MP', 'Mobile Phones'), ('AC', 'Accessories'))), ('Electronics & Home Appliances', (('CP', 'Computers & Accessories'), ('GE', 'Games & Entertainment'), ('CA', 'Cameras & Accessories'), ('TV', 'TV - Video - Audio'))), ('Bikes', (('MC', 'Motorcycles'), ('SP', 'Spare Parts'), ('BC', 'Bicycles'), ('SC', 'Scooters')))], max_length=2)),
                ('label', models.CharField(choices=[('N', 'New'), ('F', 'Featured'), ('BS', 'BEST SELLER')], default='N', max_length=2)),
                ('description', models.TextField()),
                ('album', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='model', to='shop.imagealbum')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to=shop.models.get_upload_path)),
                ('default', models.BooleanField(default=False)),
                ('width', models.FloatField(default=100)),
                ('length', models.FloatField(default=100)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.imagealbum')),
            ],
        ),
    ]
