import datetime

from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import RegisterForm, UserEditForm, PhotoForm
from .models import User, Photo, Follower, Likes, Messages, Chat
from django.contrib import messages as django_messages

# Create your views here.

def index(request):
    if request.method == 'POST':
        if request.POST.get('login'):
            return redirect('home')
        elif request.POST.get('register'):
            return redirect('register')

    return redirect('login')

def register(request):
    form = RegisterForm
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        username = request.POST['username']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            django_messages.success(request, 'Username taken')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            django_messages.info(request, ('Email taken'))
            return redirect('register')
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'main/register.html', {'form': form})

def login(request):
    if request.method == "POST":
        if request.POST.get('login'):
            username = request.POST['username']
            password = request.POST['password']
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                if password == user.password:
                    request.session['id_user'] = user.id_user
                    return redirect('home')
                else:
                    django_messages.success(request, ('Wrong password'))
                    return redirect('login')
            else:
                django_messages.success(request, ('Username does not exists'))
                return redirect('login')
        elif request.POST.get('register'):
            return redirect('register')

    return render(request, 'main/login.html')

def home(request):
    id_user = request.session.get('id_user')
    lstUserFollower = Follower.objects.filter(id_user_follower=id_user)
    users = User.objects.all()
    lstPhotoUsers = Photo.objects.filter(id_user__in=[user.id_user for user in lstUserFollower]).order_by('setup')

    num_notifiacations = 0

    likes_unseen = Likes.objects.filter(id_user=id_user).filter(status=0)
    notifications_like = {}
    for i in likes_unseen:
        u = User.objects.get(id_user=i.id_user_like).username
        notifications_like[i.id_likes] = (u + ' like your photo')
        num_notifiacations += 1

    follower_unseen = Follower.objects.filter(id_user=id_user).filter(status=0)
    notifications_fillower = {}
    for i in follower_unseen:
        u = User.objects.get(id_user=i.id_user_follower).username
        notifications_fillower[i.id_follower] = (u + ' follow you')
        num_notifiacations += 1

    messages_unseen = Messages.objects.filter(id_user_receiver=id_user).filter(status=0)
    notifications_message = {}
    for i in messages_unseen:
        u = User.objects.get(id_user=i.id_user_sender).username
        notifications_message[i.id_messages] = (u + ' sent you a message')
        num_notifiacations += 1


    if request.method == "POST":
        if request.POST.get('search'):
            search = request.POST['search']
            search_users = User.objects.filter(username__startswith=search)
            return render(request, "main/home_page.html", {
                'users': users,
                'search_users': search_users,
                'lstPhotoUsers': lstPhotoUsers,
                'id_user': id_user,
                'notifications_like': notifications_like,
                'notifications_follower': notifications_fillower,
                'notifications_message': notifications_message,
                'num_notifiacations': num_notifiacations,
            })
    return render(request, "main/home_page.html", {
        'lstPhotoUsers': lstPhotoUsers,
        'users': users,
        'id_user': id_user,
        'notifications_like': notifications_like,
        'notifications_follower': notifications_fillower,
        'notifications_message': notifications_message,
        'num_notifiacations': num_notifiacations,
    })

def profile(request):
    id_user = request.session.get('id_user')
    user = User.objects.get(id_user=id_user)

    followers = Follower.objects.filter(id_user_follower=id_user)
    user_following = User.objects.filter(id_user__in=[f.id_user for f in followers])

    following = Follower.objects.filter(id_user=id_user)
    user_followers = User.objects.filter(id_user__in=[f.id_user_follower for f in following])

    photos = Photo.objects.filter(id_user=id_user).order_by('setup')

    if request.method == 'POST':
        if request.POST.get('edit'):
            return redirect('edit')
        if request.POST.get('add_photo'):
            return redirect('add_photo')
        if request.POST.get('messages'):
            return redirect('messages', id_user=0)

    if user is not None:
        return render(request, "main/profile.html", {
            'user': user,
            'photos': photos,
            'current': True,
            'user_followers': user_followers,
            'user_following': user_following,
        })

    return render(request, "main/profile.html", {
        'photos': photos,
        'current': True,
        'user_followers': user_followers,
        'user_following': user_following,
    })

def edit(request):
    id_user = request.session.get('id_user')
    user = User.objects.get(id_user=id_user)
    form = UserEditForm(instance=user)

    if request.method == "POST":
        username = request.POST['username']
        if User.objects.filter(username=username).exclude(id_user=id_user).exists():
            django_messages.success(request, 'Username taken')
            return redirect('edit')
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        return render(request, "main/edit.html", {'form': form})

def add_photo(request):
    form = PhotoForm
    return render(request, "main/add_photo.html", {'form': form})

def upload_post(request):
    if request.method == "POST":
        p = Photo()
        p.description = request.POST.get('description')
        p.location = request.POST.get('location')
        p.photo_path = request.FILES['photo_path']
        p.effect = request.POST.get('effect')
        p.like = 0
        p.id_user = request.session.get('id_user')
        p.setup = datetime.datetime.now()
        p.save()

        data = serializers.serialize('json', [p])
        return JsonResponse({'data': data})

def photo_update(request, id):
    if request.method == 'POST':
        photo = Photo.objects.get(id_photo=id)
        photo.description = request.POST.get('description')
        photo.location = request.POST.get('location')
        photo.save()

        return HttpResponse('OK')

def photo_delete(request, id):
    if (request.method == 'DELETE'):
        photo = Photo.objects.get(id_photo=id)
        photo.delete()

        return HttpResponse('OK')

def follow(request, id):
    id_user = request.session.get('id_user')
    user_follower = User.objects.get(id_user=id)
    followers = Follower.objects.all()
    for i in followers:
        if int(i.id_user) == int(id) and int(i.id_user_follower) == int(id_user):
            django_messages.success(request, ('You already follow this user'))
            return redirect('home')
    follower = Follower()
    follower.id_user = user_follower.id_user
    follower.id_user_follower = id_user
    follower.status = 0
    follower.save()
    return redirect('home')

def profile_user(request, id):
    id_user_cur = request.session.get('id_user')
    id_user = id
    user = User.objects.get(id_user=id_user)
    photos = Photo.objects.filter(id_user=id_user).order_by('-setup')

    if id_user_cur != id_user:
        return render(request, "main/profile.html", {'user': user, 'photos': photos, 'current': False})

def like(request, id_user, id_photo):
    id_user_ = request.session.get('id_user')
    all_likes = Likes.objects.filter(id_photo=id_photo)

    for i in all_likes:
        if i.id_user == id_user and i.id_user_like == id_user_:
            django_messages.success(request, ('You already like this photo'))
            return redirect('home')

    likes = Likes()
    likes.id_user = id_user
    likes.id_photo = id_photo
    likes.id_user_like = id_user_
    likes.status = 0
    likes.save()

    photo = Photo.objects.get(id_photo=id_photo)
    photo.like += 1
    photo.save(update_fields=['like'])

    return redirect('home')

def messages(request, id_user=0):
    id_user_sender = request.session.get('id_user')

    lstUserMessages = Messages.objects.filter(id_user_sender=id_user_sender) \
                      | Messages.objects.filter(id_user_receiver=id_user_sender)
    print(lstUserMessages)
    x = set()
    for i in lstUserMessages:
        if int(i.id_user_sender) != id_user_sender:
            x.add(i.id_user_sender)
        if int(i.id_user_receiver) != id_user_sender:
            x.add(i.id_user_receiver)
    lstUsers = User.objects.filter(id_user__in=[i for i in x])
    user_obj = User.objects.get(id_user=id_user_sender)
    users = User.objects.exclude(id_user=id_user_sender)

    if id_user != 0:
        if id_user > id_user_sender:
            thread_name = f'chat_{id_user}-{id_user_sender}'
        else:
            thread_name = f'chat_{id_user_sender}-{id_user}'
        message_objs = Chat.objects.filter(thread_name=thread_name)
        return render(request, 'main/messages_user_select.html', {
            'id_user': id_user,
            'users': users,
            'messages': message_objs,
            'username': user_obj.username,
            'id_user_sender': id_user_sender,
            'lstUsers': lstUsers,
            'select': id_user,
        })

    return render(request, "main/messages.html", {
        'lstUsers': lstUsers,
        'id_user_sender': id_user_sender,
        'select': id_user})

def notifications_read_like(request, id_like):
    likes_unseen = Likes.objects.get(id_likes=id_like)
    likes_unseen.status = 1
    likes_unseen.save()
    return redirect('home')

def notifications_read_follow(request, id_follower):
    follow_unseen = Follower.objects.get(id_follower=id_follower)
    follow_unseen.status = 1
    follow_unseen.save()
    return redirect('home')

def notifications_read_messages(request, id_messages):
    messages_unseen = Messages.objects.get(id_messages=id_messages)
    messages_unseen.status = 1
    messages_unseen.save()
    return redirect('home')



