from rest_framework.routers import DefaultRouter
from django.urls import path
from django.urls import include


app_name = 'blog'

# Import Views
from apps.blog.apis import manage_category
from apps.blog.apis import manage_blog


# Router configuration
router = DefaultRouter()
router.register(r'category', manage_category.CategoryView)

urlpatterns = [
     path('', include(router.urls)),
]


urlpatterns += [
    path('create-blog/', manage_blog.CreateBlogAPIView.as_view(), name='create_blog')
]