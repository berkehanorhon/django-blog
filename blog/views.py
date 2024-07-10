from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _

from blog.models import Category
from users.models import BlogUser
from .forms import BlogPostForm
from .models import BlogPost


def search_result(request, category_name=None):
    if category_name:
        category = get_object_or_404(Category, name__iexact=category_name)
        blog_list = BlogPost.objects.filter(category=category, isPublished=True)
    else:
        blog_list = BlogPost.objects.filter(isPublished=True)

    search_query = request.GET.get('search')
    if search_query:
        blog_list = blog_list.filter(title__icontains=search_query)

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
        'search_done': search_query or category_name
    }
    return render(request, 'blog/search-result.html', context)


def view_post(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug)
    if not blog_post.isPublished and not (request.user.is_authenticated and request.user.is_superuser):
        raise Http404(_("Blog post is not published."))

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
        messages.error(request, _("You are not authorized to add blog posts."))
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
                # send_newpost_email_to_subscribers(new_post.slug) # Will send email to all subscribers when its published
                messages.success(request, _("Blog post added successfully."))
                return redirect('home')
            except Exception as e:
                messages.error(request, _(f"An error occurred: {str(e)}"))
        else:
            messages.error(request, _("Form is not valid. Please check the input."))

    else:
        form = BlogPostForm()

    categories = Category.objects.all()
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'blog/add_blog_post.html', context)


def send_newpost_email_to_subscribers(slug):
    blog_post = get_object_or_404(BlogPost, slug=slug)
    post_url = settings.SITE_URL + reverse('view_post', args=[slug])
    # TODO translation here?
    subject = f"{blog_post.author} posted a new blog!"
    message = f"{blog_post.author} posted a new blog! You can view it by clicking the link below:\n\n{post_url}"
    recipient_list = BlogUser.objects.filter(is_subscribed=True).values_list('email', flat=True)

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email="AyvBlog",
        to=[],
        bcc=recipient_list,
    )

    try:
        email.send(fail_silently=False)
    except Exception as e:
        print(e)
