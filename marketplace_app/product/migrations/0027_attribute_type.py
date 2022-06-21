# Generated by Django 3.2.13 on 2022-05-28 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_alter_productreview_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='type',
            field=models.CharField(choices=[('T', 'Text'), ('C', 'Check'), ('S', 'Select')], default='T', help_text='Field type', max_length=1, verbose_name='Field type'),
        ),
    ]