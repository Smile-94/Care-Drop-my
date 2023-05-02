from django.urls import path
from django.urls import include

app_name = 'auth'

# Import Apis/Views
from apps.authentication.apis import manage_auth

# Manage User
urlpatterns = [
    path('login/', manage_auth.Login.as_view(), name='login'),
    path('logout/', manage_auth.Logout.as_view(), name='logout'),
    path('change-password/', manage_auth.ChangePassword.as_view(), name='change-password'),
    path('signup/', manage_auth.Register.as_view(), name='signup'),
    path('refresh/', manage_auth.Refresh.as_view(), name='refresh'),
]