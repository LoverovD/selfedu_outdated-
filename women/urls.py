from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('addpage/', add_page, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('categories/<int:catid>/', categories),
    path('post/<int:post_id>/', show_post, name='post'),
    path('category/<int:cat_id>/', show_cat, name='category'),
]
