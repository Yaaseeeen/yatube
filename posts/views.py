from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View

from .forms import PostForm, CommentForm
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


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        print('self.object')
        print(self.object)
        messages.add_message(
            self.request, messages.INFO, f'Новость {self.object} удалена', extra_tags='info'
        )
        return super().get_context_data(**kwargs)


# todo
# def add_comment(request):
#     if request.method == 'POST':
#         return render(request, "post.html")


class AddCommentView(View):
    def get(self, request):
        # редирект на страницу поста
        pass

    def post(self, request):
        # добавляем комментарий
        pass


def add_comment(request, pk):
    print('request')
    print(request)

    """Добавление комментария к посту"""
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(data=request.POST)
        print('form1')
        print(form)
        if form.is_valid():
            print('form')
            print(form)
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        else:
            return render(request, 'post.html', {
                'posts': post,
                'comments': post.comments.all(),
                'comments_form': form
            })

    return redirect(reverse('post', kwargs={'pk': pk}))
