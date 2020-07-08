from django.urls import path

from . import views

urlpatterns = [
    path('account/', views.account_home, name='account_home'),
	path('logout/', views.auth_logout, name='logout'),
    path('login/', views.auth_login, name='login'),
    path('register/', views.auth_register, name='register'),
]