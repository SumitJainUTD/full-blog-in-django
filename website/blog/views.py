from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify

from .forms import TextForm, AddBlogForm
from .models import Blog, Tag, Category, Comment
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

User = get_user_model()


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


def search_blogs(request):
    search_key = request.GET.get('search', None)
    recent_blogs = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')

    if search_key:
        blogs = Blog.objects.filter(
            Q(title__icontains=search_key) |
            Q(category__title__icontains=search_key) |
            Q(user__username__icontains=search_key) |
            Q(tags__title__icontains=search_key)
        ).distinct()

        context = {
            "blogs": blogs,
            "recent_blogs": recent_blogs,
            "tags": tags,
            "search_key": search_key
        }

        return render(request, 'search.html', context)

    else:
        return redirect('home')


@login_required(login_url='login')
def my_blogs(request):
    queryset = request.user.user_blogs.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 6)
    delete = request.GET.get('delete', None)

    if delete:
        blog = get_object_or_404(Blog, pk=delete)

        if request.user.pk != blog.user.pk:
            return redirect('home')

        blog.delete()
        messages.success(request, "Your blog has been deleted!")
        return redirect('my_blogs')

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs": blogs,
        "paginator": paginator
    }

    return render(request, 'my_blogs.html', context)


@login_required(login_url='login')
def add_blog(request):
    form = AddBlogForm()

    if request.method == "POST":
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.user = user
            blog.save()
            blog.category.add(category)
            for tag in tags:
                tag_input = Tag.objects.filter(
                    title__iexact=tag.strip(),
                    slug=slugify(tag.strip())
                )
                if tag_input.exists():
                    t = tag_input.first()
                    blog.tags.add(t)

                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title=tag.strip(),
                            slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)

            messages.success(request, "Blog added successfully")
            return redirect('blog_details', slug=blog.slug)
        else:
            print(form.errors)

    context = {
        "form": form
    }
    return render(request, 'add_blog.html', context)


@login_required(login_url='login')
def update_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    form = AddBlogForm(instance=blog)

    if request.method == "POST":
        form = AddBlogForm(request.POST, request.FILES, instance=blog)

        if form.is_valid():

            if request.user.pk != blog.user.pk:
                return redirect('home')

            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.user = user

            blog.save()
            blog.category.add(category)

            for tag in tags:
                tag_input = Tag.objects.filter(
                    title__iexact=tag.strip(),
                    slug=slugify(tag.strip())
                )
                if tag_input.exists():
                    t = tag_input.first()
                    blog.tags.add(t)

                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title=tag.strip(),
                            slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)

            messages.success(request, "Blog updated successfully")
            return redirect('blog_details', slug=blog.slug)
        else:
            print(form.errors)

    context = {
        "form": form,
        "blog": blog
    }
    return render(request, 'update_blog.html', context)


@login_required(login_url='login')
def user_information(request, username):
    account = get_object_or_404(User, username=username)

    context = {
        "account": account
    }
    return render(request, 'user_information.html', context)
