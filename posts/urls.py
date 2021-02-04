from django.urls import path

from . import views

urlpatterns = (
    path("", views.index, name="index"),
    path("new/", views.new_post, name="new_post"),
    path("group/<slug:slug>/", views.group_posts, name="groups"),
    # Профайл пользователя
    path('post/<str:username>/', views.profile, name='profile'),
    # Просмотр записи
    path('post/<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('post/<str:username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
)
