# Generated by Django 4.2.3 on 2023-07-27 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='POSSlug',
            field=models.SlugField(blank=True, null=True, unique_for_date='POSPublish', verbose_name='Post Slug'),
        ),
    ]