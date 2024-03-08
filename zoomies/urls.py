from django.contrib import admin
from django.urls import path, include
from short_urls import views

from zoomies import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('short_urls.urls')),
    path('<str:short_code>/', views.redirect_to_original_url, name='redirect_to_original_url'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]