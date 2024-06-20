from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render

from .models import *


menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},]


def index(request):
    posts = Women.objects.all()
    cats = Category.objects.all()
    context = {
        "posts": posts,
        "cats": cats,
        "menu": menu,
        "title": "Главная страница",
        "selected_cat": 0,
    }
    return render(request, 'women/index.html', context=context)


def about(request):
    context = {
        "menu": menu,
        "title": "О нас"
    }
    return render(request, 'women/about.html', context=context)


def add_page(request):
    return HttpResponse('Добавить статью')


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Войти')


def show_post(request, post_id):
    post = get_object_or_404(Women, pk=post_id)
    cats = Category.objects.all()

    context = {
        'post': post,
        'cats': cats,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, "women/post.html", context=context)


def show_cat(request, cat_id):
    posts = Women.objects.filter(cat_id=cat_id)
    cats = Category.objects.all()

    if len(posts) == 0:
        raise Http404()

    context = {
        "posts": posts,
        "cats": cats,
        "menu": menu,
        "title": "Отображение по рубрикам",
        "selected_cat": cat_id,
    }
    return render(request, 'women/index.html', context=context)


def categories(request, catid):
    if catid > 100:
        return redirect('index', permanent=True)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
