# Generated by Django 3.2.13 on 2022-06-09 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20220608_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='name_en',
            field=models.CharField(max_length=150, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='shop',
            name='name_ru',
            field=models.CharField(max_length=150, null=True, verbose_name='name'),
        ),
    ]
