# Generated by Django 3.2.13 on 2022-05-04 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_merge_0008_auto_20220428_1940_0009_auto_20220429_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, help_text='User first name', max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, help_text='User last name', max_length=150, verbose_name='last name'),
        ),
    ]