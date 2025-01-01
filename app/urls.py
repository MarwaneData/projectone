from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('works/', views.works, name='works'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact, name='contact'),
    path('handle-contact/', views.handle_contact_form, name='handle_contact_form'),
    path('ai-projects/', views.ai_projects, name='ai_projects'),
]
