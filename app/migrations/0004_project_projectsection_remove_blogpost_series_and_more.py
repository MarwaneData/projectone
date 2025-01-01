# Generated by Django 5.1.4 on 2024-12-28 10:52

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_blogseries_blogtag_newsletter_blogpost_canonical_url_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(blank=True, max_length=200)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('category', models.CharField(max_length=100)),
                ('thumbnail', models.ImageField(upload_to='projects/thumbnails/')),
                ('published_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_type', models.CharField(choices=[('text', 'Text Content'), ('heading', 'Heading'), ('image', 'Image'), ('gallery', 'Image Gallery'), ('video', 'Video'), ('quote', 'Quote')], max_length=20)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('content', ckeditor.fields.RichTextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='projects/content/')),
                ('order', models.IntegerField(default=0)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='app.project')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='series',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
        migrations.DeleteModel(
            name='Newsletter',
        ),
        migrations.DeleteModel(
            name='BlogSeries',
        ),
        migrations.DeleteModel(
            name='BlogTag',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
