from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, BlogSlugHistory
from django.http import Http404
from .forms import BlogForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from profiles.models import UserProfile  # Adjust import as needed



def blog_list(request):
    blogs = Blog.objects.filter(published=True).order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'blogs': blogs})



def blog_detail(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        # Check if this slug was an old one
        redirect_entry = BlogSlugHistory.objects.filter(old_slug=slug).first()
        if redirect_entry:
            return redirect('blog:blog_detail', slug=redirect_entry.blog.slug)
        raise Http404("No Blog matches the given query.")
    
    return render(request, 'blog/blog_detail.html', {'blog': blog})


@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)

            # 🔐 Try to get or create the user profile
            user = request.user
            try:
                user_profile = user.userprofile
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(user=user)

            blog.author = user_profile
            blog.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('blog:blog_detail', slug=blog.slug)
    else:
        form = BlogForm()

    return render(request, 'blog/blog_form.html', {
        'form': form,
        'title': 'Create Blog Post',
        'submit_text': 'Publish'
    })

@login_required
def blog_edit(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated!')
            return redirect('blog:blog_detail', slug=slug)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/blog_form.html', {
        'form': form,
        'title': 'Edit Blog Post',
        'submit_text': 'Update'
    })