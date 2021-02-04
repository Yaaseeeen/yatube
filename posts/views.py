from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import View

from .forms import PostForm
from .models import Post, Group, User


# def index(request):
#     post_list = Post.objects.order_by('-pub_date').all()
#     paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
#     page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
#     page = paginator.get_page(page_number)  # получить записи с нужным смещением
#     return render(
#         request,
#         'index.html',
#         {'page': page, 'paginator': paginator}
#     )


class PostView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'index.html'
    context_object_name = 'posts'


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, "new_post.html", {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect("index")


# todo
# @login_required
# todo
class PostCreateView(CreateView, LoginRequiredMixin):
    form_class = PostForm
    template_name = 'new_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        print('post.author')
        print(post.author)
        print('post.user')
        print(self.request.user)
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


# @login_required
def post_view(request, username, pk):
    user = get_object_or_404(User, username=username)
    post = Post.objects.filter(author=user).get(pk=pk)
    return render(request, 'post.html', {'user': user, 'post': post})


# class PostDetailView(DetailView, LoginRequiredMixin):
class PostDetailView(DetailView):
    model = Post
    # user = self.request.user
    # print('userzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
    # print(user)
    context_object_name = 'post'
    template_name = 'post.html'

    def get(self, request, *args, **kwargs):
        data = super().get(request, *args, **kwargs)
        print('datasssssssssssssssssssssss')
        # print(data)
        print(self.request.user)

        return data

    # print(post)
    extra_context = {'user': model.author}

    def get_context_data(self, **kwargs):
        print(99999999999999999996666666666669)
        data = super().get_context_data(**kwargs)
        # print(data['user'].fields)
        return data

    # @property
    # def extra_context(self):
    #     return {
    #         'user': model.author
    #     }


@login_required
def post_edit(request, username, post_id):
    profil = get_object_or_404(User, username=username)
    print('datasssssssssssssssssssssprofil  ')
    print(profil)
    post = get_object_or_404(Post, pk=post_id, author=profil)
    print('datasssssssssssssssssssssss')
    print(post)
    print('datasssssssssssssssssssssss')

    if request.user != profile:
        return redirect('post', username=username, post_id=post_id)
    # добавим в form свойство files
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("post", username=request.user.username, post_id=post_id)

    return render(
        request, 'new_post.html', {'form': form, 'post': post},
    )


# todo
def add_comment(request):
    if request.method == 'POST':
        # if request.POST:
        print(88)
    return render(request, "post.html")


class AddCommentView(View):
    def get(self, request):
        # редирект на страницу поста
        pass

    def post(self, request):
        # добавляем комментарий
        pass
