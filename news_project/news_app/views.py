from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import News, Comment
from .forms import RegisterForm, CommentForm, NewsForm

def index(request):
    latest_news = News.objects.order_by('-pub_date')[:3]
    return render(request, 'news_app/index.html', {'latest_news': latest_news})

def contacts(request):
    return render(request, 'news_app/contacts.html')

def news_list(request):
    query = request.GET.get('q')
    sort = request.GET.get('sort', '-pub_date')

    news_list = News.objects.all().order_by(sort)
    if query:
        news_list = news_list.filter(title__icontains=query)

    return render(request, 'news_app/news_list.html', {'news_list': news_list})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    comments = news.comment_set.all()
    form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.news = news
                comment.user = request.user
                comment.save()
                return redirect('news_detail', pk=pk)
        else:
            form = CommentForm()
    return render(request, 'news_app/news_detail.html', {'news': news, 'comments': comments, 'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'news_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'news_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def add_news(request):
    if not request.user.is_staff:
        return redirect('index')
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm()
    return render(request, 'news_app/add_news.html', {'form': form})
