import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _

from blog.models import Category
from users.models import Subscription
from utils.decorators import author_required
from .forms import BlogPostForm
from .models import BlogPost

logger = logging.getLogger("blog" + __name__)


def search_result(request, category_name=None):
    # If category_name is not given, it will fetch all blog posts else it will fetch blog posts of that category
    blog_list = BlogPost.objects.filter(isPublished=True) if not category_name else BlogPost.objects.filter(
        category=get_object_or_404(Category, name__iexact=category_name), isPublished=True)

    search_query = request.GET.get('search')
    if search_query:
        blog_list = blog_list.filter(title__icontains=search_query)

    paginator = Paginator(blog_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'blogs': page_obj,  # not necessary, could use page_obj instead
        'page_obj': page_obj,
        'search_done': search_query or category_name
    }
    return render(request, 'blog/search-result.html', context)


def view_post(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug)
    if not blog_post.isPublished and not (request.user.is_authenticated and request.user.is_superuser):
        raise Http404(_("Blog post is not published."))

    context = {
        'blog_post': blog_post,
    }
    return render(request, 'blog/single-post.html', context)


@author_required
def add_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.save()
                messages.success(request, _("Blog post added successfully."))
                return redirect('home')
            except Exception as e:
                logger.error(f"User {request.user.id} failed to add blog post: {str(e)}")
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
    recipient_list = Subscription.objects.filter(author=blog_post.author).values_list('user__email', flat=True)
    if not recipient_list:
        return
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
        logger.error(f"Email sending failed for post {blog_post.id}: {str(e)}")
        print(e)
