from django.urls import path, re_path
from wordbucket import views

app_name = 'wordbucket'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('add_word', views.add_word, name='add_word'),
    re_path(r'^search/(\w+)$', views.search, name='search'),
    re_path(r'^(\d+)/$', views.view_word, name='detail'),
    re_path(r'^(\d+)/add_explanation$', views.add_explanation, name='add_explanation'),
    re_path(r'^(\d+)/like$', views.vote_like, name='like'),
    re_path(r'^(\d+)/dislike$', views.vote_dislike, name='dislike'),
]
