from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Group, PostForm, User


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, "new_post.html", {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect("index")


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "group.html", {"posts": posts, 'group': group})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user).order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'user': user, 'page': page, 'paginator': paginator})


def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = Post.objects.filter(author=user).get(pk=post_id)
    return render(request, 'post.html', {'user': user, 'post': post})


def post_edit(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author=user, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if not form.is_valid():
        return render(request, "new_post.html", {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return render(request, 'new_post.html', {})
