from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0006_alter_settings_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seoitem',
            name='meta_description',
            field=models.CharField(blank=True, help_text='For detail pages (products, shop etc)after meta descriptionauto adding description field of detail page', max_length=512, verbose_name='meta description'),
        ),
    ]
