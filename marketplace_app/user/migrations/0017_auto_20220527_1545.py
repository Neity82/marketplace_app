# Generated by Django 3.2.13 on 2022-05-27 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_alter_productreview_text'),
        ('user', '0016_auto_20220527_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compare',
            name='device',
        ),
        migrations.AddField(
            model_name='compare',
            name='product_id',
            field=models.ForeignKey(default=1, help_text='Product for comparison', on_delete=django.db.models.deletion.CASCADE, related_name='product_compare', to='product.product', verbose_name='product'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CompareEntity',
        ),
    ]
