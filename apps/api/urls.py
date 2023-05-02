from django.urls import path
from django.urls import include

app_name = 'api'

# App urls
from apps.authentication import urls as authentication_urls
from apps.blog import urls as blog_urls
from apps.user import urls as user_urls

urlpatterns = [
    path('auth/', include(authentication_urls, namespace='auth')),
    path('user/', include(user_urls, namespace='user')),
    path('blog/', include(blog_urls, namespace='blog')),
]
