# Generated by Django 3.2.13 on 2022-05-16 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_merge_20220515_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderentity',
            name='price_with_discount',
        ),
        migrations.AddField(
            model_name='orderentity',
            name='discounted_price',
            field=models.PositiveIntegerField(blank=True, help_text='OrderEntity discounted price', null=True, verbose_name='discounted price'),
        ),
    ]