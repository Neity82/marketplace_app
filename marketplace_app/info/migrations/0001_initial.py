# Generated by Django 3.2.13 on 2022-04-27 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='title')),
                ('text', models.TextField(verbose_name='text')),
                ('image', models.ImageField(upload_to='', verbose_name='image')),
                ('url', models.URLField(verbose_name='URL')),
                ('is_active', models.BooleanField(verbose_name='active')),
            ],
            options={
                'verbose_name': 'banner',
                'verbose_name_plural': 'banners',
                'ordering': ('is_active', 'title'),
            },
        ),
        migrations.CreateModel(
            name='SEOItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path_name', models.CharField(max_length=512, verbose_name='path name')),
                ('meta_title', models.CharField(max_length=512, verbose_name='meta title')),
                ('meta_description', models.CharField(blank=True, max_length=512, verbose_name='meta description')),
                ('title', models.CharField(blank=True, max_length=512, verbose_name='meta description')),
            ],
            options={
                'verbose_name': 'SEO item',
                'verbose_name_plural': 'SEO items',
                'ordering': ('path_name',),
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('value', models.PositiveIntegerField(default=0, verbose_name='value')),
            ],
            options={
                'verbose_name': 'settings',
                'verbose_name_plural': 'settings',
                'ordering': ('name',),
            },
        ),
    ]