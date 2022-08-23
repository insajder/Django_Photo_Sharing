from django.contrib import admin
from .models import User, Photo, Follower, Likes, Messages, Chat

# Register your models here.

# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'username')

@admin.register(Photo)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id_photo', 'id_user', 'description', 'location')

@admin.register(Follower)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id_follower', 'id_user', 'id_user_follower')

@admin.register(Likes)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id_likes', 'id_user', 'id_photo', 'id_user_like')

@admin.register(Messages)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id_messages', 'id_user_receiver', 'id_user_sender')

@admin.register(Chat)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id_chat', 'thread_name', 'sender')
