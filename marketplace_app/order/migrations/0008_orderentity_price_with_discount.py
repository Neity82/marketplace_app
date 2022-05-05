# Generated by Django 3.2.13 on 2022-05-05 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20220504_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderentity',
            name='price_with_discount',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='OrderEntity price with discount', verbose_name='price with discount'),
            preserve_default=False,
        ),
    ]