from django.shortcuts import render
from django.http import HttpResponse
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

def about(request):
    # return HttpResponse('<h1>About</h1>')
    return render(request, 'app/about.html')