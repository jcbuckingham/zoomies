from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from short_urls import views as short_url_views
from users import views as user_url_views
from zoomies import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/short_urls/', include('short_urls.urls')),
    path('', user_url_views.register),
    path('logout/', user_url_views.logout),
    path('login/', user_url_views.login),
    path('openapi/', TemplateView.as_view(template_name='openapi_spec.yaml', content_type='text/yaml'), name='openapi-schema'),
    path('<str:short_code>/', short_url_views.redirect_to_original_url, name='redirect_to_original_url'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]