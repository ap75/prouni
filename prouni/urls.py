from django.urls import path, include

from web.admin import admin_site


urlpatterns = [
    path('admin/', admin_site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('web.urls')),
]
