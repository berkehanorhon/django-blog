# Generated by Django 5.0.6 on 2024-07-10 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_blogpost_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='publish_date',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Publish Date'),
        ),
    ]
