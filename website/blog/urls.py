from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('blogs/', blogs, name='blogs'),
    path('category_blogs/<str:slug>', category_blogs, name='category_blogs'),
    path('tag_blogs/<str:slug>', tag_blogs, name='tag_blogs'),
    path('blog_details/<str:slug>', blog_details, name='blog_details'),
    path('like_blog/<int:pk>/', like_blog, name='like_blog'),
    path('search_blogs/', search_blogs, name='search_blogs'),

]