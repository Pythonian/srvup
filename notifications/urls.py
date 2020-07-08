from django.urls import path

from . import views


urlpatterns = [
    path('', views.all, name='notifications_all'),
    path('ajax/', views.get_notifications_ajax, name='get_notifications_ajax'),
    path('<id>/', views.read, name='notifications_read'),
]
