# Generated by Django 4.2 on 2023-06-20 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='orderhistory',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='history_order', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mahsulot_olchov',
            name='mahsulot_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='number', to='products.mahsulotlar'),
        ),
    ]
