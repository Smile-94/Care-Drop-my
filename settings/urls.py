from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.views import serve

#Import module for sweagger generator
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.urls import include



# Api urls
from apps.api import urls as api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('care-drop/v1/', include(api_urls, namespace='api')),
]

# for serve static files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, view=serve)

#Define a schema_view using get_schema_view
schema_view = get_schema_view(
   openapi.Info(
      title="Care-Drop API",
      default_version='v1',
      description="Test description",
      contact=openapi.Contact(email="mshossen75@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


#Add a swagger URL
urlpatterns += [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]