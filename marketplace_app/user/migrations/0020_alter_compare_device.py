# Generated by Django 3.2.13 on 2022-06-02 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_auto_20220530_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compare',
            name='device',
            field=models.CharField(blank=True, help_text='cookie device value', max_length=255, null=True, verbose_name='device'),
        ),
    ]
