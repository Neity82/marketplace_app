# Generated by Django 3.2.13 on 2022-05-19 13:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='compare',
            name='user_id',
            field=models.ForeignKey(help_text='A user who compares products', on_delete=django.db.models.deletion.CASCADE, related_name='user_compare', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
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
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, help_text='User phone', max_length=16, validators=[django.core.validators.RegexValidator(message='Invalid format', regex='^\\d{10}$')], verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='userproductview',
            name='user_id',
            field=models.ForeignKey(help_text='The user who viewed the product', on_delete=django.db.models.deletion.CASCADE, related_name='user_view', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]