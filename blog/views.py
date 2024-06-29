from django.shortcuts import render
from blog.models import BlogPost, Category
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
# Create your views here.

def index(request):
    context = {
        'message': 'Hello, World how u doin!'
    }
    return render(request, 'blog/index.html', context)

def search_result(request, category_name=None):
    if category_name:
        category = get_object_or_404(Category, name__iexact=category_name)
        blogs = BlogPost.objects.filter(category=category)
    else:
        blogs = BlogPost.objects.all()

    context = {
        'blogs': blogs,
         'search_done': category_name
    }
    return render(request, 'blog/search-result.html', context)

def view_post(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug)

    blog_data = {
        'category': blog_post.category.name,
        'date': blog_post.created_at.strftime("%b %d '%y"),
        'title': blog_post.title,
        'description': blog_post.content,
        'image_url': blog_post.image,
        'author_name': str(blog_post.author),
        'author_image_url': blog_post.author.avatar,
        'post_url': '#'
    }

    context = {
        'blog_data': blog_data
    }
    return render(request, 'blog/single-post.html', context)
