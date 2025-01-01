from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F
from .models import BlogPost, BlogCategory, Project, ProjectSection
from django.views.generic import ListView
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.conf import settings
import logging
from django.template.loader import render_to_string
from django.urls import reverse

logger = logging.getLogger(__name__)

def index(request):
    # Get latest 3 blog posts for the index page
    latest_blogs = BlogPost.objects.all().order_by('-published_date')[:3]
    
    # Get recent projects
    recent_projects = Project.objects.all().order_by('-published_date')[:4]
    
    context = {
        'latest_blogs': latest_blogs,
        'recent_projects': recent_projects,
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def works(request):
    projects = Project.objects.all().order_by('-published_date')
    return render(request, 'works.html', {'projects': projects})

def blogs(request):
    categories = BlogCategory.objects.all()
    posts = BlogPost.objects.select_related('category').prefetch_related(
        'sections'
    ).order_by('-published_date')
    
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    context = {
        'categories': categories,
        'posts': posts,
    }
    return render(request, 'blogs.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    # Increment view count
    post.views = F('views') + 1
    post.save()
    
    # Refresh from database to get the updated view count
    post.refresh_from_db()
    
    # Get related posts
    related_posts = post.related_posts.all()[:2]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog.html', context)

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    sections = project.sections.all()
    
    context = {
        'project': project,
        'sections': sections,
    }
    return render(request, 'project.html', context)

class BlogListView(ListView):
    model = BlogPost
    template_name = 'blogs.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        queryset = BlogPost.objects.all()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(subtitle__icontains=q) |
                Q(sections__content__icontains=q)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = BlogPost.objects.filter(is_featured=True)[:3]
        context['categories'] = BlogCategory.objects.all()
        return context

def contact_page(request):
    if request.method == 'POST':
        # Here you can add form processing logic
        # For example, sending emails
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('app:contact')
    return render(request, 'contact.html')

def ai_projects(request):
    # Filter projects with AI category
    ai_projects = Project.objects.filter(category__icontains='AI').order_by('-published_date')
    return render(request, 'ai_projects.html', {'ai_projects': ai_projects})

def contact(request):
    if request.method == 'POST':
        try:
            # Get all POST data
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            # Validate the data
            if not all([name, email, subject, message]):
                print("\nValidation Error: Missing Fields")
                messages.error(request, "Please fill in all required fields.")
                return render(request, 'contact.html')
            # Prepare email content
            email_content = f"""
New Contact Form Submission

From: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""
            print("\nAttempting to send email...")
            
            try:
                # Send email
                send_mail(
                    subject=f"Contact Form: {subject}",
                    message=email_content,
                    from_email='noreplay.mtph@gmail.com',
                    recipient_list=['contact@maroneai.com'],
                    fail_silently=False,
                )
                print("Email sent successfully!")
                messages.success(request, "Thank you! Your message has been sent successfully.")
                
            except Exception as e:
                print(f"\nEmail Error:")
                print(f"Type: {type(e).__name__}")
                print(f"Message: {str(e)}")
                messages.error(request, "Sorry, there was a problem sending your message. Please try again later.")
                
        except Exception as e:
            print(f"\nForm Processing Error:")
            print(f"Type: {type(e).__name__}")
            print(f"Message: {str(e)}")
            messages.error(request, "An error occurred while processing your request.")
        
        # Return the same page with the messages
        return render(request, 'contact.html')
    
    # GET request - just show the form
    return render(request, 'contact.html')

def handle_contact_form(request):
    if request.method == 'POST':
        try:
            # Get all POST data
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            # Validate the data
            if not all([name, email, subject, message]):
                messages.error(request, "Please fill in all required fields.")
                return redirect(request.META.get('HTTP_REFERER', reverse('app:index')))

            # Prepare email content using template
            html_message = render_to_string('email/contact_email.html', {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message
            })

            # Create EmailMessage object
            email_message = EmailMessage(
                subject=f"Contact Form: {subject}",
                body=html_message,
                from_email='noreplay.mtph@gmail.com',
                to=['contact@maroneai.com'],
                reply_to=[email]
            )
            email_message.content_subtype = "html"  


            # Send email
            try:
                email_message.send(fail_silently=False)
                success_msg = "Thank you! Your message has been sent successfully"
                messages.success(request, success_msg)
                
            except Exception as e:
                logger.error(f"Email sending failed: {str(e)}")
                messages.error(request, "Sorry, there was a problem sending your message. Please try again later.")
                
        except Exception as e:
            logger.error(f"Form processing error: {str(e)}")
            messages.error(request, "An error occurred while processing your request.")
        
        # Redirect back to the page they came from
        return redirect(request.META.get('HTTP_REFERER', reverse('app:index')))
    
    # If not POST, redirect to home
    return redirect('app:index')

def handler404(request, exception):
    return render(request, '404.html', status=404)
