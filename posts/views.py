from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.base import View

from .forms import PostForm
from .models import Post, Group, User


class PostView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'index.html'
    context_object_name = 'posts'


class PostCreateView(CreateView):
    form_class = PostForm
    template_name = 'new_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


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


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post.html'

    def get(self, request, *args, **kwargs):
        data = super().get(request, *args, **kwargs)
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data


class PostEditView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'new_post.html'

    @property
    def success_url(self):
        return reverse('post', kwargs={'username': self.object, 'pk': self.object.pk})


# todo
def add_comment(request):
    if request.method == 'POST':
        return render(request, "post.html")


class AddCommentView(View):
    def get(self, request):
        # редирект на страницу поста
        pass

    def post(self, request):
        # добавляем комментарий
        pass
