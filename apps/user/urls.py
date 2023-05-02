from django.urls import path
from django.urls import include


app_name = 'user'

# Import Views/Apis
from apps.user.apis import manage_account
from apps.user.apis import manage_user

# Manage My Profile
urlpatterns = [
     path('profile/', manage_account.Profile.as_view(), name='profile'),
     path('profile-update/', manage_account.ProfileUpdate.as_view(), name='profile-update'),
]

# Manage User
urlpatterns += [
    path('add-user/', manage_user.AddUser.as_view(), name='add_user'),
    path('update-user/<int:pk>/', manage_user.UpdateUser.as_view(), name='update_user'),
    path('user-list/', manage_user.UserList.as_view(), name='user_details'),
    path('user-details/<int:pk>/', manage_user.UserDetails.as_view(), name='user_details'),
    path('delete-user/<int:pk>/', manage_user.UserDelete.as_view(), name='delete-user'),
]
