# Generated by Django 3.2.13 on 2022-05-20 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20220520_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='quality_policy',
            field=models.CharField(blank=True, max_length=50, verbose_name='quality policy'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='refund_policy',
            field=models.CharField(blank=True, max_length=50, verbose_name='refund policy'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='shipping_policy',
            field=models.CharField(blank=True, max_length=50, verbose_name='shipping and returns policy'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='support_policy',
            field=models.CharField(blank=True, max_length=50, verbose_name='support policy'),
        ),
    ]
