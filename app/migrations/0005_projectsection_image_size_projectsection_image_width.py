# Generated by Django 5.1.4 on 2024-12-28 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_project_projectsection_remove_blogpost_series_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectsection',
            name='image_size',
            field=models.CharField(blank=True, choices=[('full-width', 'Full Width'), ('medium', 'Medium'), ('small', 'Small')], default='medium', max_length=20),
        ),
        migrations.AddField(
            model_name='projectsection',
            name='image_width',
            field=models.CharField(blank=True, help_text='Optional. Example: 500px or 80%', max_length=10),
        ),
    ]
