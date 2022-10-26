from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TextForm
from .models import Blog, Tag, Category, Comment
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


def category_blogs(request, slug):
    category = Category.objects.get(slug=slug)
    queryset = category.category_blogs.all()
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

    all_blogs = Blog.objects.order_by('-created_date')[:5]
    context = {
        "blogs": blogs,
        "tags": tags,
        "paginator": paginator,
        "all_blogs": all_blogs
    }
    return render(request, 'category_blogs.html', context)


def tag_blogs(request, slug):
    tag = Tag.objects.get(slug=slug)
    queryset = tag.tag_blogs.all()
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
    return render(request, 'tag_blogs.html', context)


def blog_details(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    all_blogs = Blog.objects.order_by('-created_date')[:5]
    categories = Category.objects.filter(category_blogs__id=blog.id)
    related_blogs = Blog.objects.filter(category__in=categories)
    liked_by = request.user in blog.likes.all()

    if request.method == 'POST' and request.user.is_authenticated:
        form = TextForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                user=request.user,
                blog=blog,
                text=form.cleaned_data.get('text')
            )
            return redirect('blog_details', slug=slug)


    context = {
        "blog": blog,
        "all_blogs": all_blogs,
        "related_blogs": related_blogs[:5],
        "liked_by": liked_by
    }
    return render(request, 'blog_details.html', context)

@login_required(login_url='/')
def like_blog(request, pk):
    print("aaaaa")
    context = {}
    blog = get_object_or_404(Blog, pk=pk)
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        context['liked'] = False
    else:
        blog.likes.add(request.user)
        context['liked'] = True
    context['likes_count'] = blog.likes.all().count()
    return JsonResponse(context, safe=False)