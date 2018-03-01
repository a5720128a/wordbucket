from django.urls import path, re_path
from wordbucket import views

urlpatterns = [
    path('', views.home_page, name='home'),
]
