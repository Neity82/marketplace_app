# Generated by Django 3.2.13 on 2022-05-05 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_orderentity_price_with_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderentity',
            name='price_with_discount',
            field=models.PositiveIntegerField(blank=True, help_text='OrderEntity price with discount', null=True, verbose_name='price with discount'),
        ),
    ]
