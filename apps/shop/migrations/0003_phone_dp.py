# Generated by Django 4.2.3 on 2023-07-31 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_order_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='dp',
            field=models.ImageField(default='shop/gallery/Apple-iPhone-8-Plus-Gold.jpg', upload_to='shop/gallery'),
        ),
    ]
