from django.urls import path, re_path
from django.contrib.auth import views as auth_views
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
    
    # auth part
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    re_path(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    # csv
    re_path(r'^(\d+)/import$', views.import_csv, name='import'),
    re_path(r'^(\d+)/export$', views.export_csv, name='export'),
]
