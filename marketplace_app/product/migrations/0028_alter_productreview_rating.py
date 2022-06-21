# Generated by Django 3.2.13 on 2022-06-03 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_productreview_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Product rating', null=True, verbose_name='rating'),
        ),
    ]