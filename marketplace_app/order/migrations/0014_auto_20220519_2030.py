# Generated by Django 3.2.13 on 2022-05-19 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0013_auto_20220516_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='user_id',
            field=models.ForeignKey(help_text='Cart user', on_delete=django.db.models.deletion.CASCADE, related_name='cart_user', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(help_text='Delivery name', max_length=50, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user_id',
            field=models.ForeignKey(help_text='Order user', on_delete=django.db.models.deletion.CASCADE, related_name='order_info', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
