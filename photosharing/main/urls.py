from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path("home/", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path("edit/", views.edit, name="edit"),
    path("add_photo/", views.add_photo, name="add_photo"),
    path("upload_post/", views.upload_post, name="upload_post"),
    path("photo_delete/<int:id>", views.photo_delete, name="photo_delete"),
    path("photo_update/<int:id>", views.photo_update, name="photo_update"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("profile_user/<int:id>", views.profile_user, name="profile_user"),
    path("like/<int:id_user>/<int:id_photo>", views.like, name="like"),
    path("messages/<int:id_user>", views.messages, name="messages"),
    path("notifications_read_like/<int:id_like>", views.notifications_read_like, name="notifications_read_like"),
    path("notifications_read_follow/<int:id_follower>", views.notifications_read_follow, name="notifications_read_follow"),
    path("notifications_read_messages/<int:id_messages>", views.notifications_read_messages, name="notifications_read_messages"),
]