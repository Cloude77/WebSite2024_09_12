# Generated by Django 5.1.4 on 2024-12-09 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, unique_for_date=True),
        ),
    ]