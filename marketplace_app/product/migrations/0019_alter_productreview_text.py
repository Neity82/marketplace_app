# Generated by Django 3.2.13 on 2022-05-16 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_merge_20220515_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='text',
            field=models.TextField(default='', help_text='', max_length=1500, verbose_name='review content'),
        ),
    ]
