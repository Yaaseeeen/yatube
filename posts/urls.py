from django.urls import path

from . import views
from django.conf.urls import handler404, handler500

handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa
urlpatterns = (
    path("", views.PostView.as_view(), name="index"),
    path("new/", views.new_post, name="new_post"),
    # path("new/", views.PostCreateView.as_view(), name="new_post"),
    path("group/<slug:slug>/", views.group_posts, name="groups"),
    # Профайл пользователя
    path('<str:username>/', views.profile, name='profile'),
    # Просмотр записи
    path('<str:username>/<int:pk>/', views.post_view, name='post'),
    # path('<str:username>/<int:pk>/', views.PostDetailView.as_view(), name='post'),
    path('<str:username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
)
