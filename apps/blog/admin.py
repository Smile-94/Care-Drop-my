from django.contrib import admin

# Models Classes
from apps.blog.models import BlogCategory
from apps.blog.models import BlogPost
from apps.blog.models import Like
from apps.blog.models import Bookmark

# Register your models here.
@admin.register(BlogCategory)
class BlogCatagoryAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    search_fields = ('name',)
    list_display = ('name', 'created_at', 'updated_at')
    list_per_page = 10

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    search_fields = ('author', 'category','status')
    list_filter = ('category', 'status', 'is_active')
    list_display = ('author', 'status', 'published_at', 'created_at', 'updated_at')
    list_per_page = 50

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    search_fields = ('like_by',)
    list_filter = ('created_at', 'updated_at')
    list_display = ('like_by', 'like_of','created_at', 'updated_at')
    list_per_page = 50

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    search_fields = ('bookm_by',)
    list_filter = ('created_at', 'updated_at')
    list_display = ('bookmark_by', 'bookmark_of','created_at', 'updated_at')
    list_per_page = 50