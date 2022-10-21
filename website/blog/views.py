from django.shortcuts import render, redirect
from .models import Blog, Tag
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

# Create your views here.


def home(request):
    blogs = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    context = {
        "blogs": blogs,
        "tags": tags
    }
    return render(request, 'home.html', context=context)


def blogs(request):
    queryset = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 2)

    print(page)
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    print(blogs)
    print(paginator.per_page)
    print(paginator.count)
    print("blogs.number" + str(blogs.number))
    context = {
        "blogs": blogs,
        "tags": tags,
        "paginator": paginator
    }
    return render(request, 'blog.html', context)
