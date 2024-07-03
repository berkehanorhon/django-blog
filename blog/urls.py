from django.urls import path
import blog.views

urlpatterns = [
    path("", blog.views.search_result, name="home"),
    path('search/', blog.views.search_result, name='search_result'),
    path('search/<str:category_name>/', blog.views.search_result, name='search_result_by_category'),
    path("post/<slug:slug>/", blog.views.view_post, name="view_post"),
    path("post/add", blog.views.add_blog_post, name="add_blog_post"),
]
