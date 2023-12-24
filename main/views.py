from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import PostForm, RegistrationForm, UserForm
from .models import Post, Topic, Message


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('main')

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("main")
        else:
            messages.error(request, "Incorrect Password")

    context = {'page': page}
    return render(request, 'login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect("main")


def registerPage(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("main")
        else:
            messages.error(request, "An error occurred")

    return render(request, 'login_register.html', {'form': form})


def main(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    posts = Post.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(host__username__icontains=q) |
                                Q(description__icontains=q)
                                )

    topics = Topic.objects.all()
    post_count = posts.count()
    post_messages = Message.objects.filter(Q(post__topic__name__icontains=q))

    context = {'posts': posts, 'topics': topics,
               'post_count': post_count, 'post_messages': post_messages}

    return render(request, "main.html", context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    post_messages = user.message_set.all()
    topics = Topic.objects.all()
    post_count = posts.count()

    context = {'user': user, 'posts': posts,
               'post_messages': post_messages, 'topics': topics, 'post_count': post_count}
    return render(request, "main/profile.html", context)


def postPage(request, pk):
    post = Post.objects.get(id=pk)
    post_messages = post.message_set.all().order_by('-created')
    participants = post.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            post=post,
            body=request.POST.get('body')
        )
        post.participants.add(request.user)
        return redirect("post", pk=post.id)

    context = {'post': post, 'post_messages': post_messages, 'participants': participants}
    return render(request, "main/post.html", context)


@login_required(login_url='login')
def createPost(request):
    form = PostForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Post.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        return redirect('main')

    context = {'form': form, 'topics': topics, 'create': True}
    return render(request, 'main/post_form.html', context)


@login_required(login_url='login')
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    topics = Topic.objects.all()
    form = PostForm(instance=post)

    if request.user != post.host:
        return HttpResponse("You are not allowed to edit this post")

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        post.name = request.POST.get('name')
        post.description = request.POST.get('description')
        post.topic = topic
        post.save()
        return redirect('main')

    context = {'form': form, 'topics': topics, 'post': post, 'create': False}

    return render(request, "main/post_form.html", context)


@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)

    if request.user != post.host:
        return HttpResponse("You are not allowed to delete this post")

    if request.method == "POST":
        post.delete()
        return redirect('main')

    return render(request, "delete.html", {'obj': post})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed to delete this post")

    if request.method == "POST":
        message.delete()
        return redirect('main')

    return render(request, "delete.html", {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    context = {'form': form}
    return render(request, 'main/profile_edit.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    topics = Topic.objects.filter(name__icontains=q)

    context = {'topics': topics}
    return render(request, 'main/topics.html', context)
