# Generated by Django 3.2.13 on 2022-05-24 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0004_auto_20220523_1051'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='settings',
            options={'ordering': ('description',), 'verbose_name': 'settings', 'verbose_name_plural': 'settings'},
        ),
        migrations.AddField(
            model_name='settings',
            name='description',
            field=models.CharField(default='', max_length=50, verbose_name='description'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='settings',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='value',
            field=models.CharField(max_length=150, verbose_name='value'),
        ),
    ]