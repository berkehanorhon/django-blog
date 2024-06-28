from django.urls import path
import blog.views

urlpatterns = [
    path("", blog.views.index, name="home"),
    path("/searchresult", blog.views.search_result, name="search result"),
    path("/singlepost", blog.views.view_post, name="view post")
]
