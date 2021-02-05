from django.urls import path

from . import views
from .views import PostDetailView

handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa
urlpatterns = (
    path("", views.PostView.as_view(), name="index"),
    path("new/", views.PostCreateView.as_view(), name="new_post"),
    # todo
    # path("group/<slug:slug>/", views.group_posts, name="groups"),
    # Профайл пользователя
    path('<str:username>/', views.profile, name='profile'),
    # Просмотр записи
    path('<str:username>/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('<str:username>/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
)
