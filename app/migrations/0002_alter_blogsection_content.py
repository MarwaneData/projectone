# Generated by Django 5.1.4 on 2024-12-18 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogsection',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
