# Generated by Django 3.2.13 on 2022-06-08 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_merge_20220606_1424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit',
            name='unit',
        ),
        migrations.AddField(
            model_name='attribute',
            name='title_en',
            field=models.CharField(help_text='Category title', max_length=50, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='title_ru',
            field=models.CharField(help_text='Category title', max_length=50, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='category',
            name='title_en',
            field=models.CharField(help_text='Category title', max_length=50, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='category',
            name='title_ru',
            field=models.CharField(help_text='Category title', max_length=50, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='product',
            name='long_description_en',
            field=models.TextField(help_text='Product long description', max_length=1500, null=True, verbose_name='long description'),
        ),
        migrations.AddField(
            model_name='product',
            name='long_description_ru',
            field=models.TextField(help_text='Product long description', max_length=1500, null=True, verbose_name='long description'),
        ),
        migrations.AddField(
            model_name='product',
            name='short_description_en',
            field=models.CharField(help_text='Product short description', max_length=150, null=True, verbose_name='short description'),
        ),
        migrations.AddField(
            model_name='product',
            name='short_description_ru',
            field=models.CharField(help_text='Product short description', max_length=150, null=True, verbose_name='short description'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_en',
            field=models.CharField(help_text='Product title', max_length=150, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_ru',
            field=models.CharField(help_text='Product title', max_length=150, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='tag',
            name='title_en',
            field=models.CharField(help_text='Tag title', max_length=50, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='tag',
            name='title_ru',
            field=models.CharField(help_text='Tag title', max_length=50, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='unit',
            name='title',
            field=models.CharField(default=0, max_length=16, verbose_name='unit title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unit',
            name='title_en',
            field=models.CharField(max_length=16, null=True, verbose_name='unit title'),
        ),
        migrations.AddField(
            model_name='unit',
            name='title_ru',
            field=models.CharField(max_length=16, null=True, verbose_name='unit title'),
        ),
    ]
