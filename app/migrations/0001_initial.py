# Generated by Django 5.1.4 on 2024-12-18 18:42

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Blog Categories',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(blank=True, max_length=200)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('reading_time', models.IntegerField(default=5, help_text='Reading time in minutes')),
                ('views', models.IntegerField(default=0)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('author_name', models.CharField(max_length=100)),
                ('author_title', models.CharField(max_length=100)),
                ('author_image', models.ImageField(blank=True, upload_to='blog/authors/')),
                ('author_bio', models.TextField(blank=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.blogcategory')),
            ],
            options={
                'ordering': ['-published_date'],
            },
        ),
        migrations.CreateModel(
            name='BlogSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_type', models.CharField(choices=[('text', 'Text Content'), ('code', 'Code Block'), ('image', 'Image'), ('quote', 'Quote'), ('list', 'Bullet List'), ('timeline', 'Timeline')], max_length=20)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('content', ckeditor.fields.RichTextField(blank=True)),
                ('code', models.TextField(blank=True)),
                ('code_language', models.CharField(blank=True, max_length=50)),
                ('image', models.ImageField(blank=True, upload_to='blog/content/')),
                ('order', models.IntegerField(default=0)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='app.blogpost')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='RelatedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0)),
                ('main_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_posts', to='app.blogpost')),
                ('related_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_to', to='app.blogpost')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]