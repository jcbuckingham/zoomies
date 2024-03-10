from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView

from short_urls import views as short_url_views
from users import views as user_url_views
from zoomies import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Zoomies Documentation",
        default_version="v1",
        description="Note: Use the api/short_urls documentation to create and maintain the shortened urls for your user.",
        url='/openapi/',
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/short_urls/', include('short_urls.urls')),
    path('', user_url_views.register),
    path('logout/', user_url_views.logout),
    path('login/', user_url_views.login),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('openapi/', TemplateView.as_view(template_name='openapi_spec.yaml', content_type='text/yaml'), name='openapi-schema'),
    path('<str:short_code>/', short_url_views.redirect_to_original_url, name='redirect_to_original_url'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]