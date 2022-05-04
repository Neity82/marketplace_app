# Generated by Django 3.2.13 on 2022-04-27 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('user', '0002_auto_20220427_0944'),
    ]

    operations = [
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='datetime of addition')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_view', to='product.product', verbose_name='product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_view', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Просмотреть',
                'verbose_name_plural': 'Views',
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='Compare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_compare', to='product.product', verbose_name='product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_compare', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Compare',
                'verbose_name_plural': 'Compares',
            },
        ),
    ]