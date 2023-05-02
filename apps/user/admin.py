from django.contrib import admin

# Import User apps Models
from apps.user.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ('id',)
    search_fields = ("email", "full_name")
    list_filter = ("is_active", "is_staff", "is_superuser")
    list_display = ('id','email','full_name','contact_number','is_staff','is_active','is_moderator')
    list_per_page = 50



