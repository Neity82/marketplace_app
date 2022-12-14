# Generated by Django 3.2.13 on 2022-04-29 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_customuser_phone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userproductview',
            options={'ordering': ['-datetime'], 'verbose_name': 'viewed product', 'verbose_name_plural': 'viewed products'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, help_text='User first name', max_length=150, verbose_name='имя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, help_text='User last name', max_length=150, verbose_name='фамилия'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='middle_name',
            field=models.CharField(blank=True, help_text='User middle name', max_length=150, verbose_name='middle name'),
        ),
    ]
