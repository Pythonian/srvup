from django.urls import path

from . import views


urlpatterns = [
    path('<id>/', views.comment_thread, name='comment_thread'),
    path('create/', views.comment_create_view, name='comment_create'),
]
