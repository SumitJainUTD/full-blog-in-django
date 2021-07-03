from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

posts =[
    {
        'author': 'Sumit',
        'title': "First Post",
        'content': "First content",
        'date_posted': "Jun 28, 2021"
    },
    {
        'author': 'Ramit',
        'title': "Second Post",
        'content': "Second content",
        'date_posted': "Jun 29, 2021"
    }
]

def home(request):
    context = {
        "posts": Post.objects.all()
    }
    return render(request, 'app/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'app/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post


def about(request):
    # return HttpResponse('<h1>About</h1>')
    return render(request, 'app/about.html')