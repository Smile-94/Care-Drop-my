from django.db import models
from django.utils import timezone

# Import Django Tagable Field for keywords
from taggit.managers import TaggableManager


# Import Models
from apps.user.models import User
from apps.common.models import CustomID
from apps.common.models import BaseModel

# Create your models here.

class BlogCategory(BaseModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class BlogPost(BaseModel):
    # Choices for the status of the blog post
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('rejected', 'Rejected'),
        ('published', 'Published'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_author')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='blog_reviewer', null=True)
    category = models.ManyToManyField(BlogCategory)
    title = models.CharField(max_length=200)
    content = models.TextField()
    post_image = models.ImageField(upload_to='blog_post/', blank=True, null=True)
    keywords = TaggableManager(blank=True)
    published_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_active = models.BooleanField(default=True) # This fields used to soft-delete the blog post


    # This function wll save the published date when blogpost status is published
    def publish(self):
        if self.status == 'published':
            self.published_date = timezone.now()
            self.save()
    
    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.title[:30]

class Like(BaseModel):
    like_by= models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'liker')
    like_of = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name= 'likes')

    def __str__(self):
        return str(self.likes_by)

class Bookmark(BaseModel):
    bookmark_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'savers')
    bookmark_of = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name= 'bookmarks')

    def __str__(self):
        return str(self.bookmarks_by)
    