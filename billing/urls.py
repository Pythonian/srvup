from django.urls import path

from . import views


urlpatterns = [
    path('', views.billing_history, name='billing_history'),
    path('upgrade/', views.upgrade, name='account_upgrade'),
    path('cancel/', views.cancel_subscription, name='cancel_subscription'),
]
