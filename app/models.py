from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.utils import timezone

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Categories"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    
    # Meta information
    reading_time = models.IntegerField(help_text="Reading time in minutes", default=5)
    views = models.IntegerField(default=0)
    published_date = models.DateTimeField(auto_now_add=True)
    
    # Author information
    author_name = models.CharField(max_length=100)
    author_title = models.CharField(max_length=100)
    author_image = models.ImageField(upload_to='blog/authors/', blank=True)
    author_bio = models.TextField(blank=True)
    
    # SEO Fields
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords")
    canonical_url = models.URLField(blank=True, help_text="Canonical URL if different from current URL")
    is_featured = models.BooleanField(default=False)
    
    # Social Sharing
    social_image = models.ImageField(upload_to='blog/social/', blank=True, help_text="Image for social media sharing")
    twitter_card = models.CharField(max_length=100, blank=True, help_text="Twitter handle")
    
    # Analytics
    read_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    
    def get_reading_time(self):
        """Calculate reading time based on content length"""
        word_count = len(' '.join([section.content for section in self.sections.all()]).split())
        return max(1, round(word_count / 200))  # Assuming 200 words per minute

    def get_next_post(self):
        """Get next post in the same category"""
        return BlogPost.objects.filter(
            category=self.category,
            published_date__gt=self.published_date
        ).order_by('published_date').first()

    def get_prev_post(self):
        """Get previous post in the same category"""
        return BlogPost.objects.filter(
            category=self.category,
            published_date__lt=self.published_date
        ).order_by('-published_date').first()

    def increment_view_count(self):
        """Increment view count atomically"""
        from django.db.models import F
        self.views = F('views') + 1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        """Get the canonical URL for the post"""
        from django.urls import reverse
        return reverse('app:blog_detail', kwargs={'slug': self.slug})

    def get_similar_posts(self):
        """Get similar posts based on tags"""
        return BlogPost.objects.filter(tags__in=self.tags.all()).exclude(id=self.id).distinct()[:3]

    def get_first_image(self):
        """Get the first image from blog sections or return None"""
        image_section = self.sections.filter(section_type='image').first()
        return image_section.image if image_section else None

    def get_excerpt(self):
        """Get a short excerpt from the first text section"""
        text_section = self.sections.filter(section_type='text').first()
        if text_section and text_section.content:
            return text_section.content[:150] + '...'
        return ''

    class Meta:
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class BlogSection(models.Model):
    SECTION_TYPES = (
        ('text', 'Text Content'),
        ('code', 'Code Block'),
        ('image', 'Image'),
        ('quote', 'Quote'),
        ('list', 'Bullet List'),
        ('timeline', 'Timeline'),
    )

    blog = models.ForeignKey(BlogPost, related_name='sections', on_delete=models.CASCADE)
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    title = models.CharField(max_length=200, blank=True)
    content = RichTextField(blank=True, config_name='default')
    code = models.TextField(blank=True)
    code_language = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='blog/content/', blank=True)
    order = models.IntegerField(default=0)

    def get_formatted_content(self):
        """Convert line breaks to paragraphs"""
        if self.content and self.section_type == 'text':
            paragraphs = self.content.split('\n\n')
            return ''.join([f'<p>{p.strip()}</p>' for p in paragraphs if p.strip()])
        return self.content

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.blog.title} - Section {self.order}"

class RelatedPost(models.Model):
    main_post = models.ForeignKey(BlogPost, related_name='related_posts', on_delete=models.CASCADE)
    related_post = models.ForeignKey(BlogPost, related_name='related_to', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

class Project(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=100)  # e.g., "UX case study"
    thumbnail = models.ImageField(upload_to='projects/thumbnails/')
    published_date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProjectSection(models.Model):
    SECTION_TYPES = (
        ('text', 'Text Content'),
        ('heading', 'Heading'),
        ('image', 'Image'),
        ('gallery', 'Image Gallery'),
        ('video', 'Video'),
        ('quote', 'Quote'),
    )

    project = models.ForeignKey(Project, related_name='sections', on_delete=models.CASCADE)
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    title = models.CharField(max_length=200, blank=True)
    content = RichTextField(blank=True)
    image = models.ImageField(upload_to='projects/content/', blank=True)
    order = models.IntegerField(default=0)
    
    IMAGE_SIZES = (
        ('full-width', 'Full Width'),
        ('medium', 'Medium'),
        ('small', 'Small'),
    )
    
    image_size = models.CharField(
        max_length=20, 
        choices=IMAGE_SIZES, 
        default='medium',
        blank=True
    )
    image_width = models.CharField(
        max_length=10, 
        blank=True, 
        help_text="Optional. Example: 500px or 80%"
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.project.title} - Section {self.order}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
