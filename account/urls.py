from django.urls import path
from account import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('', views.home, name='home'),
    path('vippackage/', views.vip_package, name='vippackage'),
    path('news/', views.news_, name='news'),
    path('my_account/', views.my_account, name='my_account'),
]
