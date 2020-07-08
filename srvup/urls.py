from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from django.contrib import admin
from django.views.generic import TemplateView

from .views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', 
        TemplateView.as_view(template_name='company/contact_us.html'), 
        name='contact_us'),
    path('', home, name='home'),
    path('projects/', include('videos.urls')),
    path('notifications/', include('notifications.urls')),
    path('comment/', include('comments.urls')),
    path('billing/', include('billing.urls')),
    path('auth/', include('accounts.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
