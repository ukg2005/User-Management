from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import BlogPost, Category
from .forms import BlogPostForm

def ensure_default_categories():
    if Category.objects.count() == 0:
        default_categories = [
            ('Mental Health', 'mental-health'),
            ('Heart Disease', 'heart-disease'),
            ('Covid19', 'covid19'),
            ('Immunization', 'immunization')
        ]
        for name, slug in default_categories:
            Category.objects.create(name=name, slug=slug)
    return Category.objects.all()

@login_required
def doctor_blog_list(request):
    user_type = request.user.user_type.strip() if request.user.user_type else ""
    
    if user_type != 'doctor':
        raise PermissionDenied("Only doctors can access this page.")
    
    blogs = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/doctor_blog_list.html', {'blogs': blogs})

@login_required
def create_blog(request):
    user_type = request.user.user_type.strip() if request.user.user_type else ""
    
    if user_type != 'doctor':
        raise PermissionDenied("Only doctors can create blog posts.")
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request, "Blog post created successfully.")
            return redirect('doctor_blog_list')
    else:
        form = BlogPostForm()
    
    categories = ensure_default_categories()
    return render(request, 'blog/create_blog.html', {'form': form, 'categories': categories})

@login_required
def edit_blog(request, blog_id):
    user_type = request.user.user_type.strip() if request.user.user_type else ""
    
    if user_type != 'doctor':
        raise PermissionDenied("Only doctors can edit blog posts.")
    
    blog_post = get_object_or_404(BlogPost, id=blog_id, author=request.user)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post updated successfully.")
            return redirect('doctor_blog_list')
    else:
        form = BlogPostForm(instance=blog_post)
    
    return render(request, 'blog/edit_blog.html', {'form': form, 'blog': blog_post})

@login_required
def delete_blog(request, blog_id):
    user_type = request.user.user_type.strip() if request.user.user_type else ""
    
    if user_type != 'doctor':
        raise PermissionDenied("Only doctors can delete blog posts.")
    
    blog_post = get_object_or_404(BlogPost, id=blog_id, author=request.user)
    
    if request.method == 'POST':
        blog_post.delete()
        messages.success(request, "Blog post deleted successfully.")
        return redirect('doctor_blog_list')
    
    return render(request, 'blog/delete_blog.html', {'blog': blog_post})

@login_required
def patient_blog_list(request):
    message_list = list(messages.get_messages(request))
    for message in message_list:
        messages.add_message(request, message.level, message.message)
    
    categories = ensure_default_categories()
    category_slug = request.GET.get('category', '')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        blogs = BlogPost.objects.filter(
            category=category, 
            is_draft=False
        ).order_by('-created_at')
    else:
        blogs = BlogPost.objects.filter(is_draft=False).order_by('-created_at')
    
    return render(request, 'blog/patient_blog_list.html', {
        'blogs': blogs, 
        'categories': categories,
        'current_category': category_slug
    })

@login_required
def blog_detail(request, blog_id):
    blog_post = get_object_or_404(BlogPost, id=blog_id)
    
    if blog_post.is_draft and blog_post.author != request.user:
        raise PermissionDenied("This blog post is not published yet.")
    
    return render(request, 'blog/blog_detail.html', {'blog': blog_post})
