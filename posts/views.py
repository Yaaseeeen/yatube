from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView

from .models import Post, Group, PostForm


def index(request):
    latest = Post.objects.order_by("-pub_date")[:11]
    return render(request, "index.html", {"posts": latest})


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


class PostView(CreateView):
    form_class = PostForm
    success_url = ""
    template_name = "new_post.html"
