# Generated by Django 3.2.13 on 2022-04-28 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20220428_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='text',
            field=models.TextField(default='', help_text='', max_length=1500, verbose_name='review content'),
        ),
    ]