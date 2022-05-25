# Generated by Django 3.2.13 on 2022-05-24 19:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0026_alter_productreview_text'),
        ('order', '0014_auto_20220519_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='count',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='stock_id',
        ),
        migrations.AddField(
            model_name='cart',
            name='device',
            field=models.CharField(blank=True, help_text='cookie device value', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user_id',
            field=models.ForeignKey(blank=True, help_text='Cart user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_user', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.CreateModel(
            name='CartEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_entity', to='order.cart', verbose_name="cart's ")),
                ('stock', models.ForeignKey(blank=True, help_text='Cart stock', on_delete=django.db.models.deletion.CASCADE, related_name='cart_entity', to='product.stock')),
            ],
            options={
                'verbose_name': 'cart entity',
                'verbose_name_plural': 'cart entities',
                'ordering': ['-id'],
            },
        ),
    ]
