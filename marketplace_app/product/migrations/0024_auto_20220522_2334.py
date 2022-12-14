# Generated by Django 3.2.13 on 2022-05-22 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_auto_20220521_1536'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='productimage',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='attributevalue',
            name='value',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='value'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='text',
            field=models.TextField(default='', help_text='', max_length=1500, verbose_name='review content'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='unit',
            field=models.CharField(max_length=16, verbose_name='unit'),
        ),
    ]
