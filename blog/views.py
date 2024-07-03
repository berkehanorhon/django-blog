from blog.models import BlogPost, Category
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm

def index(request):
    context = {
        'message': 'Hello, World how u doin!'
    }
    return render(request, 'blog/index.html', context)

def search_result(request, category_name=None):
    if category_name:
        category = get_object_or_404(Category, name__iexact=category_name)
        blog_list = BlogPost.objects.filter(category=category)
    else:
        blog_list = BlogPost.objects.all()

    paginator = Paginator(blog_list, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'blogs': page_obj,
        'page_obj': page_obj,
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

@login_required
def add_blog_post(request):
    user = request.user
    if not user.is_author:
        messages.error(request, "You are not authorized to add blog posts.")
        return redirect('home')

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            category = form.cleaned_data['category']
            image = form.cleaned_data['image']

            try:
                new_post = BlogPost(
                    title=title,
                    author=user,
                    category=category,
                    content=content,
                    image=image
                )
                new_post.save()
                messages.success(request, "Blog post added successfully.")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "Form is not valid. Please check the input.")

    else:
        form = BlogPostForm()

    categories = Category.objects.all()
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'blog/add_blog_post.html', context)