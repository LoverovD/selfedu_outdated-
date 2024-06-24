from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *


menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},]


class WomenHome(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = {"selected_cat": 0, 'title': 'Главная страница'}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['cats'] = Category.objects.all()
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return Women.objects.filter(is_published=True)


# def index(request):
#     posts = Women.objects.all()
#     cats = Category.objects.all()
#     context = {
#         "posts": posts,
#         "cats": cats,
#         "menu": menu,
#         "title": "Главная страница",
#         "selected_cat": 0,
#     }
#     return render(request, 'women/index.html', context=context)


def about(request):
    context = {
        "menu": menu,
        "title": "О нас"
    }
    return render(request, 'women/about.html', context=context)


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['cats'] = Category.objects.all()
        context['title'] = 'Добавление статьи'
        return context

# def add_page(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('index')

#     else:
#         form = AddPostForm()

#     cats = Category.objects.all()
#     context = {
#         "form": form,
#         "cats": cats,
#         "menu": menu,
#         "title": "Добавление записи"
#     }

#     return render(request, 'women/addpage.html', context=context)


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Войти')


class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['cats'] = Category.objects.all()
        context['selected_cat'] = context['post'].cat_id
        context['title'] = context['post']
        return context

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     cats = Category.objects.all()

#     context = {
#         'post': post,
#         'cats': cats,
#         'menu': menu,
#         'title': post.title,
#         'selected_cat': post.cat_id,
#     }

#     return render(request, "women/post.html", context=context)


class WomenCategory(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['cats'] = Category.objects.all()
        context['selected_cat'] = context['posts'][0].cat_id
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


# def show_cat(request, cat_slug):
#     cat_id = Category.objects.get(slug=cat_slug).pk
#     posts = Women.objects.filter(cat_id=cat_id)
#     cats = Category.objects.all()

#     if len(posts) == 0:
#         raise Http404()

#     context = {
#         "posts": posts,
#         "cats": cats,
#         "menu": menu,
#         "title": "Отображение по рубрикам",
#         "selected_cat": cat_id,
#     }
#     return render(request, 'women/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
