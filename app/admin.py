from django.contrib import admin
from .models import BlogPost, BlogCategory, BlogSection, RelatedPost, Project, ProjectSection

class BlogSectionInline(admin.StackedInline):
    model = BlogSection
    extra = 1

class RelatedPostInline(admin.TabularInline):
    model = RelatedPost
    fk_name = 'main_post'
    extra = 1

class ProjectSectionInline(admin.StackedInline):
    model = ProjectSection
    extra = 1

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date', 'reading_time', 'views')
    list_filter = ('category', 'published_date')
    search_fields = ('title', 'subtitle')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlogSectionInline, RelatedPostInline]

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
@admin.register(BlogSection)
class BlogSectionAdmin(admin.ModelAdmin):
    list_display = ('blog', 'section_type', 'order')
    list_filter = ('section_type', 'blog')
    ordering = ('blog', 'order')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectSectionInline]

