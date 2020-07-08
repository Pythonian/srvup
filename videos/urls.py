from django.urls import path

from . import views

urlpatterns = [
    path('', views.category_list, name='projects'),
    path('<cat_slug>/', views.category_detail, name='project_detail'),
    path('<cat_slug>/<vid_slug>/', views.video_detail, name='video_detail'),
]