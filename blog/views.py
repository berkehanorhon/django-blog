from django.shortcuts import render
from blog.models import BlogPost, Category
from django.views.generic import ListView
from django.shortcuts import render
# Create your views here.

def index(request):
    context = {
        'message': 'Hello, World how u doin!'
    }
    return render(request, 'blog/index.html', context)

def search_result(request):
    blogs = [
        {
            'category': 'Business',
            'date': "Jul 5th '22",
            'title': 'What is the son of Football Coach John Gruden, Deuce Gruden doing Now?',
            'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Distinctio placeat exercitationem magni voluptates dolore. Tenetur fugiat voluptates quas.',
            'image_url': 'assets/img/post-landscape-6.jpg',
            'author_name': 'Wade Warren',
            'author_image_url': 'assets/img/person-2.jpg',
            'post_url': 'single-post.html'
        },
        {
            'category': 'Business',
            'date': "Jul 5th '22",
            'title': 'What is the son of Football Coach John Gruden, Deuce Gruden doing Now?',
            'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Distinctio placeat exercitationem magni voluptates dolore. Tenetur fugiat voluptates quas.',
            'image_url': 'assets/img/post-landscape-6.jpg',
            'author_name': 'Wade Warren',
            'author_image_url': 'assets/img/person-2.jpg',
            'post_url': 'single-post.html'
        },
        # Diğer blog objeleri...
    ]

    context = {
        'blogs': blogs
    }
    return render(request, 'blog/search-result.html', context)

def view_post(request):
    blog_data = {
        'category': 'Business',
        'date': "Jul 5th '22",
        'title': '13 Amazing Poems from Shel Silverstein with Valuable Life Lessons',
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Ratione officia sed, suscipit distinctio, numquam omnis quo fuga ipsam quis inventore voluptatum recusandae culpa.',
        'image_url': 'assets/img/post-landscape-1.jpg',
        'author_name': 'John Doe',
        'author_image_url': 'assets/img/author.jpg',
        'post_url': '#'
    }

    context = {
        'blog_data': blog_data
    }
    return render(request, 'blog/single-post.html', context)